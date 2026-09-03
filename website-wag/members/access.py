from functools import wraps

from django.shortcuts import redirect


def is_active_member(user):
    """True only if `user` is authenticated AND has a Member row with
    status == 'attivo'. Defensive against a User with no Member at all
    (e.g. a superuser created via `createsuperuser`), which would otherwise
    raise RelatedObjectDoesNotExist on `user.member`."""
    if not user.is_authenticated:
        return False
    member = getattr(user, 'member', None)
    return member is not None and member.status == 'attivo'


def active_member_required(view_func):
    """Redirects to the homepage instead of LOGIN_URL: OTP-registered members
    get an unusable password (see members.views.verify_otp), so there is no
    real login form to send a gated-out visitor to."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not is_active_member(request.user):
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped
