from django.urls import path

from . import login_views, views

app_name = 'members'

urlpatterns = [
    path('register/', views.register_submit, name='register-submit'),
    path('register/resend/', views.resend_otp, name='otp-resend'),
    path('register/verify/', views.verify_otp, name='otp-verify'),
    path('register/cancel/', views.cancel_registration, name='register-cancel'),
    path('login/', login_views.login_request, name='login-request'),
    path('login/resend/', login_views.login_resend, name='login-resend'),
    path('login/verify/', login_views.login_verify, name='login-verify'),
    path('login/cancel/', login_views.login_cancel, name='login-cancel'),
    path('logout/', login_views.logout_view, name='logout'),
]
