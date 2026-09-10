from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse


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
    """Not-authenticated visitors go to the dedicated /login/ page (the
    site's OTP-based login for returning members, see members.login_views/
    members.pages), preserving `next` so they land back here after logging
    in. Authenticated but non-active members (inattivo/sospeso) still just
    bounce to '/' — unlike missing authentication, that's not something
    logging in again would fix."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), login_url=reverse('login-page'))
        if not is_active_member(request.user):
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped
