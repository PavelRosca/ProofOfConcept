from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django_ratelimit.decorators import ratelimit

from .forms import LoginRequestForm, OTPVerifyForm
from .models import MAX_OTP_ATTEMPTS, MAX_RESENDS, OTP_TTL, RESEND_COOLDOWN, LoginOTP, generate_otp
from .views import GENERIC_OTP_ERROR, RATE_LIMIT_ERROR, SEND_FAILURE_ERROR, _client_ip, _form_errors, _redirect_next


def _send_login_otp_email(otp_obj, code):
    subject = 'Il tuo codice di accesso'
    message = (
        f"Ciao,\n\n"
        f"Il tuo codice di accesso è: {code}\n"
        f"Il codice scade tra {int(OTP_TTL.total_seconds() // 60)} minuti.\n\n"
        "Se non hai richiesto questo codice, ignora pure questa email."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [otp_obj.email], fail_silently=False)


def _send_no_account_email(otp_obj):
    """Sent instead of a login code when no account exists for this address —
    keeps the HTTP response identical to a real login request so the form
    can't be used to enumerate members by email (see login_request())."""
    subject = 'Nessun account trovato'
    message = (
        "Ciao,\n\n"
        "Non risulta nessun account registrato con questo indirizzo email. "
        "Se vuoi iscriverti, visita la homepage e compila il modulo di registrazione.\n\n"
        "Se non hai richiesto questa email, ignorala pure."
    )
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [otp_obj.email], fail_silently=False)


def pending_login_key(group, request):
    # django_ratelimit encodes the key as a string internally — the session value
    # is an int (LoginOTP pk), so it must be cast here or ratelimiting 500s.
    return str(request.session.get('pending_login_id') or 'anon')


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='5/h', method='POST', block=False)
def login_request(request):
    """Step 1: issue (or resend) a hashed login OTP by email — without revealing
    whether the address has an account (mirrors register_submit(), inverted:
    there, a code is poisoned if the account *already* exists; here, it's
    poisoned if the account *doesn't* exist)."""
    if getattr(request, 'limited', False):
        request.session['login_errors'] = {'__all__': [RATE_LIMIT_ERROR]}
        return _redirect_next(request)

    form = LoginRequestForm(request.POST)
    if not form.is_valid():
        request.session['login_errors'] = _form_errors(form)
        request.session['login_values'] = request.POST.dict()
        return _redirect_next(request)

    if form.cleaned_data.get('website'):
        # Honeypot tripped — behave exactly like a real submission.
        return _redirect_next(request)

    email = form.cleaned_data['email']
    now = timezone.now()

    pending = LoginOTP.objects.filter(
        email=email, verified_at__isnull=True, expires_at__gt=now
    ).order_by('-created_at').first()

    if pending:
        if now - pending.last_sent_at < RESEND_COOLDOWN:
            request.session['login_errors'] = {
                '__all__': ['Abbiamo già inviato un codice a questo indirizzo. Attendi prima di richiederne uno nuovo.']
            }
            request.session['login_values'] = request.POST.dict()
            return _redirect_next(request)
        if pending.resend_count >= MAX_RESENDS:
            request.session['login_errors'] = {
                '__all__': ['Troppe richieste per questo indirizzo. Riprova più tardi.']
            }
            return _redirect_next(request)
        otp_obj = pending
        otp_obj.resend_count += 1
    else:
        otp_obj = LoginOTP(email=email)

    # Checked here (not in LoginRequestForm.clean_email) so the HTTP response
    # stays identical whether or not the address has an account — re-checked
    # again in login_verify() since existence can change between the two steps.
    account_exists = User.objects.filter(username__iexact=email).exists()

    code = generate_otp()
    otp_obj.otp_hash = make_password(code)
    otp_obj.expires_at = now + OTP_TTL
    otp_obj.last_sent_at = now
    otp_obj.attempts = 0
    otp_obj.ip_address = _client_ip(request)

    try:
        if account_exists:
            _send_login_otp_email(otp_obj, code)
        else:
            _send_no_account_email(otp_obj)
    except Exception:
        request.session['login_errors'] = {'__all__': [SEND_FAILURE_ERROR]}
        request.session['login_values'] = request.POST.dict()
        return _redirect_next(request)

    otp_obj.save()
    request.session['pending_login_id'] = otp_obj.pk
    return _redirect_next(request)


@require_http_methods(['POST'])
def login_cancel(request):
    """Lets the user back out of the login OTP step (e.g. wrong email)."""
    otp_id = request.session.pop('pending_login_id', None)
    if otp_id:
        try:
            otp_obj = LoginOTP.objects.get(pk=otp_id, verified_at__isnull=True)
            request.session['login_values'] = {'email': otp_obj.email}
        except LoginOTP.DoesNotExist:
            pass
    return _redirect_next(request)


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='3/h', method='POST', block=False)
def login_resend(request):
    """Reissue a fresh login OTP against the already-pending, session-bound attempt."""
    if getattr(request, 'limited', False):
        request.session['login_otp_errors'] = [RATE_LIMIT_ERROR]
        return _redirect_next(request)

    otp_id = request.session.get('pending_login_id')
    if not otp_id:
        return _redirect_next(request)

    now = timezone.now()
    try:
        otp_obj = LoginOTP.objects.get(pk=otp_id, verified_at__isnull=True)
    except LoginOTP.DoesNotExist:
        request.session.pop('pending_login_id', None)
        return _redirect_next(request)

    if now - otp_obj.last_sent_at < RESEND_COOLDOWN:
        request.session['login_otp_errors'] = ['Attendi prima di richiedere un nuovo codice.']
        return _redirect_next(request)
    if otp_obj.resend_count >= MAX_RESENDS:
        request.session['login_otp_errors'] = ['Hai raggiunto il numero massimo di richieste. Riprova più tardi.']
        return _redirect_next(request)

    # Resend always re-sends for whichever branch login_request() already
    # decided — it doesn't disclose anything new about account existence.
    account_exists = User.objects.filter(username__iexact=otp_obj.email).exists()
    code = generate_otp()
    otp_obj.otp_hash = make_password(code)
    otp_obj.expires_at = now + OTP_TTL
    otp_obj.last_sent_at = now
    otp_obj.attempts = 0
    otp_obj.resend_count += 1

    try:
        if account_exists:
            _send_login_otp_email(otp_obj, code)
        else:
            _send_no_account_email(otp_obj)
    except Exception:
        request.session['login_otp_errors'] = [SEND_FAILURE_ERROR]
        return _redirect_next(request)

    otp_obj.save()
    return _redirect_next(request)


@require_http_methods(['POST'])
@ratelimit(key='ip', rate='15/h', method='POST', block=False)
@ratelimit(key=pending_login_key, rate='8/10m', method='POST', block=False)
def login_verify(request):
    """Step 2: check the submitted code; on success, log the matching User in."""
    if getattr(request, 'limited', False):
        request.session['login_otp_errors'] = [RATE_LIMIT_ERROR]
        return _redirect_next(request)

    otp_id = request.session.get('pending_login_id')
    if not otp_id:
        return _redirect_next(request)

    form = OTPVerifyForm(request.POST)
    if not form.is_valid():
        request.session['login_otp_errors'] = [GENERIC_OTP_ERROR]
        return _redirect_next(request)

    now = timezone.now()
    try:
        otp_obj = LoginOTP.objects.get(pk=otp_id, verified_at__isnull=True)
    except LoginOTP.DoesNotExist:
        request.session.pop('pending_login_id', None)
        request.session['login_otp_errors'] = [GENERIC_OTP_ERROR]
        return _redirect_next(request)

    if now > otp_obj.expires_at or otp_obj.attempts >= MAX_OTP_ATTEMPTS:
        request.session['login_otp_errors'] = [GENERIC_OTP_ERROR]
        return _redirect_next(request)

    code = form.cleaned_data['code']
    if not check_password(code, otp_obj.otp_hash):
        otp_obj.attempts += 1
        otp_obj.save(update_fields=['attempts'])
        request.session['login_otp_errors'] = [GENERIC_OTP_ERROR]
        return _redirect_next(request)

    # Re-checked here, not just at request time: the account may have been
    # created/deleted/deactivated in between. is_active is checked explicitly
    # because login() is called directly below, bypassing authenticate()'s
    # usual enforcement of that flag.
    user = User.objects.filter(username__iexact=otp_obj.email, is_active=True).first()

    otp_obj.verified_at = now
    otp_obj.save(update_fields=['verified_at'])
    request.session.pop('pending_login_id', None)

    if user is None:
        request.session['login_otp_errors'] = [GENERIC_OTP_ERROR]
        return _redirect_next(request)

    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return _redirect_next(request)


@require_http_methods(['POST'])
def logout_view(request):
    """POST-only by design (OWASP/Django convention) — a bare GET logout link
    is a drive-by-logout / logout-CSRF vector."""
    logout(request)
    return _redirect_next(request)
