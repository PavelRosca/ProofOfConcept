from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit

from core.models import Member

from .forms import OTPVerifyForm, RegistrationForm
from .models import MAX_OTP_ATTEMPTS, MAX_RESENDS, OTP_TTL, RESEND_COOLDOWN, RegistrationOTP, generate_otp

GENERIC_OTP_ERROR = 'Codice non valido o scaduto.'
SEND_FAILURE_ERROR = 'Non è stato possibile inviare il codice. Riprova tra qualche minuto.'
RATE_LIMIT_ERROR = 'Troppe richieste. Riprova tra qualche minuto.'


def _client_ip(request):
    return request.META.get('REMOTE_ADDR')


def _redirect_next(request):
    """Preserves the current language prefix (site uses i18n_patterns) instead of
    hardcoding '/', which would silently bounce an /en/ visitor back to the default
    language homepage. 'next' is a same-origin path the template sets from
    request.path — validated to rule out an open-redirect via a forged POST."""
    next_url = request.POST.get('next', '/')
    if not url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        next_url = '/'
    return redirect(next_url)


def _form_errors(form):
    """Plain dict[str, list[str]] — session-JSON-safe (form.errors values are ErrorList, not list)."""
    return {field: list(msgs) for field, msgs in form.errors.items()}


def _safe_next_param(request):
    """Validates a GET '?next=' the same way _redirect_next validates POST's
    'next' — used by the login/join page views to accept a gated-redirect
    target (see members.access.active_member_required) without risking an
    open redirect via a forged query string."""
    next_param = request.GET.get('next')
    if next_param and url_has_allowed_host_and_scheme(
        next_param, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return next_param
    return None


def _send_otp_email(otp_obj, code):
    subject = 'Il tuo codice di verifica'
    message = (
        f"Ciao {otp_obj.first_name},\n\n"
        f"Il tuo codice di verifica è: {code}\n"
        f"Il codice scade tra {int(OTP_TTL.total_seconds() // 60)} minuti.\n\n"
        "Se non hai richiesto questo codice, ignora pure questa email."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [otp_obj.email], fail_silently=False)


def _send_already_registered_email(otp_obj):
    """Sent instead of an OTP code when the address already has an account — keeps
    the HTTP response identical to a fresh registration so the form can't be used to
    enumerate registered members by email (membership reveals political affiliation)."""
    subject = 'Hai già un account'
    message = (
        f"Ciao {otp_obj.first_name},\n\n"
        "Risulta che questo indirizzo email sia già registrato. Prova ad accedere invece di registrarti di nuovo.\n\n"
        "Se non hai richiesto questa email, ignorala pure."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [otp_obj.email], fail_silently=False)


def pending_registration_key(group, request):
    # django_ratelimit encodes the key as a string internally — the session value
    # is an int (RegistrationOTP pk), so it must be cast here or ratelimiting 500s.
    return str(request.session.get('pending_registration_id') or 'anon')


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='5/h', method='POST', block=False)
def register_submit(request):
    """Step 1: validate personal info, issue (or resend) a hashed OTP by email."""
    if getattr(request, 'limited', False):
        request.session['registration_errors'] = {'__all__': [RATE_LIMIT_ERROR]}
        return _redirect_next(request)

    form = RegistrationForm(request.POST)
    if not form.is_valid():
        request.session['registration_errors'] = _form_errors(form)
        request.session['registration_values'] = request.POST.dict()
        return _redirect_next(request)

    if form.cleaned_data.get('website'):
        # Honeypot tripped — behave exactly like a real submission (same
        # redirect, no error) so a bot can't tell it was dropped, but skip
        # creating any RegistrationOTP or sending any email.
        return _redirect_next(request)

    data = form.cleaned_data
    email = data['email']
    now = timezone.now()

    pending = RegistrationOTP.objects.filter(
        email=email, verified_at__isnull=True, expires_at__gt=now
    ).order_by('-created_at').first()

    if pending:
        if now - pending.last_sent_at < RESEND_COOLDOWN:
            request.session['registration_errors'] = {
                '__all__': ['Abbiamo già inviato un codice a questo indirizzo. Attendi prima di richiederne uno nuovo.']
            }
            request.session['registration_values'] = request.POST.dict()
            return _redirect_next(request)
        if pending.resend_count >= MAX_RESENDS:
            request.session['registration_errors'] = {
                '__all__': ['Troppe richieste per questo indirizzo. Riprova più tardi.']
            }
            return _redirect_next(request)
        otp_obj = pending
        otp_obj.resend_count += 1
    else:
        otp_obj = RegistrationOTP(email=email)

    otp_obj.first_name = data['first_name']
    otp_obj.last_name = data['last_name']
    otp_obj.phone = data['phone']
    otp_obj.address_street = data['address_street']
    otp_obj.address_number = data['address_number']
    otp_obj.address_postal_code = data['address_postal_code']
    otp_obj.address_city = data['address_city']
    otp_obj.address_province = data['address_province']

    # Checked here (not in RegistrationForm.clean_email) so the HTTP response and
    # redirect stay identical whether or not the address is already registered —
    # see _send_already_registered_email(). verify_otp() re-checks before creating
    # the account, so a never-disclosed code simply fails like any wrong code.
    already_registered = User.objects.filter(username__iexact=email).exists()

    code = generate_otp()
    otp_obj.otp_hash = make_password(code)
    otp_obj.expires_at = now + OTP_TTL
    otp_obj.last_sent_at = now
    otp_obj.attempts = 0
    otp_obj.ip_address = _client_ip(request)

    try:
        if already_registered:
            _send_already_registered_email(otp_obj)
        else:
            _send_otp_email(otp_obj, code)
    except Exception:
        request.session['registration_errors'] = {'__all__': [SEND_FAILURE_ERROR]}
        request.session['registration_values'] = request.POST.dict()
        return _redirect_next(request)

    otp_obj.save()
    request.session['pending_registration_id'] = otp_obj.pk
    return _redirect_next(request)


@require_http_methods(['POST'])
def cancel_registration(request):
    """Lets the user back out of the OTP step to fix a typo in step 1 (e.g. wrong
    email) instead of being stuck with only 'resend' — pre-fills step 1 from the
    pending row's already-submitted values so they don't have to retype everything."""
    otp_id = request.session.pop('pending_registration_id', None)
    if otp_id:
        try:
            otp_obj = RegistrationOTP.objects.get(pk=otp_id, verified_at__isnull=True)
            request.session['registration_values'] = {
                'first_name': otp_obj.first_name,
                'last_name': otp_obj.last_name,
                'email': otp_obj.email,
                'phone': otp_obj.phone,
                'address_street': otp_obj.address_street,
                'address_number': otp_obj.address_number,
                'address_postal_code': otp_obj.address_postal_code,
                'address_city': otp_obj.address_city,
                'address_province': otp_obj.address_province,
            }
        except RegistrationOTP.DoesNotExist:
            pass
    return _redirect_next(request)


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='3/h', method='POST', block=False)
def resend_otp(request):
    """Reissue a fresh OTP against the already-pending, session-bound registration."""
    if getattr(request, 'limited', False):
        request.session['otp_errors'] = [RATE_LIMIT_ERROR]
        return _redirect_next(request)

    otp_id = request.session.get('pending_registration_id')
    if not otp_id:
        return _redirect_next(request)

    now = timezone.now()
    try:
        otp_obj = RegistrationOTP.objects.get(pk=otp_id, verified_at__isnull=True)
    except RegistrationOTP.DoesNotExist:
        request.session.pop('pending_registration_id', None)
        return _redirect_next(request)

    if now - otp_obj.last_sent_at < RESEND_COOLDOWN:
        request.session['otp_errors'] = ['Attendi prima di richiedere un nuovo codice.']
        return _redirect_next(request)
    if otp_obj.resend_count >= MAX_RESENDS:
        request.session['otp_errors'] = ['Hai raggiunto il numero massimo di richieste. Riprova più tardi.']
        return _redirect_next(request)

    code = generate_otp()
    otp_obj.otp_hash = make_password(code)
    otp_obj.expires_at = now + OTP_TTL
    otp_obj.last_sent_at = now
    otp_obj.attempts = 0
    otp_obj.resend_count += 1

    try:
        _send_otp_email(otp_obj, code)
    except Exception:
        request.session['otp_errors'] = [SEND_FAILURE_ERROR]
        return _redirect_next(request)

    otp_obj.save()
    return _redirect_next(request)


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='15/h', method='POST', block=False)
@ratelimit(key=pending_registration_key, rate='8/10m', method='POST', block=False)
def verify_otp(request):
    """Step 2: check the submitted code; on success, create User+Member and log in."""
    if getattr(request, 'limited', False):
        request.session['otp_errors'] = [RATE_LIMIT_ERROR]
        return _redirect_next(request)

    otp_id = request.session.get('pending_registration_id')
    if not otp_id:
        return _redirect_next(request)

    form = OTPVerifyForm(request.POST)
    if not form.is_valid():
        request.session['otp_errors'] = [GENERIC_OTP_ERROR]
        return _redirect_next(request)

    now = timezone.now()
    try:
        otp_obj = RegistrationOTP.objects.get(pk=otp_id, verified_at__isnull=True)
    except RegistrationOTP.DoesNotExist:
        request.session.pop('pending_registration_id', None)
        request.session['otp_errors'] = [GENERIC_OTP_ERROR]
        return _redirect_next(request)

    if now > otp_obj.expires_at or otp_obj.attempts >= MAX_OTP_ATTEMPTS:
        request.session['otp_errors'] = [GENERIC_OTP_ERROR]
        return _redirect_next(request)

    code = form.cleaned_data['code']
    if not check_password(code, otp_obj.otp_hash):
        otp_obj.attempts += 1
        otp_obj.save(update_fields=['attempts'])
        request.session['otp_errors'] = [GENERIC_OTP_ERROR]
        return _redirect_next(request)

    with transaction.atomic():
        if User.objects.filter(username__iexact=otp_obj.email).exists():
            otp_obj.verified_at = now
            otp_obj.save(update_fields=['verified_at'])
            request.session.pop('pending_registration_id', None)
            request.session['otp_errors'] = [GENERIC_OTP_ERROR]
            return _redirect_next(request)

        user = User.objects.create_user(
            username=otp_obj.email,
            email=otp_obj.email,
            first_name=otp_obj.first_name,
            last_name=otp_obj.last_name,
            password=None,
        )
        Member.objects.create(
            user=user,
            status='attivo',
            phone=otp_obj.phone,
            address_street=otp_obj.address_street,
            address_number=otp_obj.address_number,
            address_postal_code=otp_obj.address_postal_code,
            address_city=otp_obj.address_city,
            address_province=otp_obj.address_province,
        )
        otp_obj.verified_at = now
        otp_obj.save(update_fields=['verified_at'])

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    request.session.pop('pending_registration_id', None)
    request.session['registration_success'] = True
    return _redirect_next(request)
