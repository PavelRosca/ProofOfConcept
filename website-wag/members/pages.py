from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .views import _safe_next_param


@require_http_methods(['GET'])
def login_page(request):
    """Dedicated /login/ page for returning members — mirrors the session-flash
    context HomePage.get_context() used to build when this lived in a homepage
    anchor section, just relocated here."""
    if request.user.is_authenticated:
        return redirect('/sciarrone/')

    context = {
        'pending_login': bool(request.session.get('pending_login_id')),
        'login_errors': request.session.pop('login_errors', None),
        'login_values': request.session.pop('login_values', None),
        'login_otp_errors': request.session.pop('login_otp_errors', None),
        'login_next': _safe_next_param(request),
    }
    return render(request, 'site/login.html', context)


@require_http_methods(['GET'])
def join_page(request):
    """Dedicated /join/ page for new registrations — mirrors the session-flash
    context HomePage.get_context() used to build when this lived in a homepage
    anchor section, just relocated here."""
    if request.user.is_authenticated:
        return redirect('/sciarrone/')

    context = {
        'pending_registration': bool(request.session.get('pending_registration_id')),
        'registration_errors': request.session.pop('registration_errors', None),
        'registration_values': request.session.pop('registration_values', None),
        'otp_errors': request.session.pop('otp_errors', None),
    }
    return render(request, 'site/join.html', context)
