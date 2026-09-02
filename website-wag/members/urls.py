from django.urls import path

from . import views

app_name = 'members'

urlpatterns = [
    path('register/', views.register_submit, name='register-submit'),
    path('register/resend/', views.resend_otp, name='otp-resend'),
    path('register/verify/', views.verify_otp, name='otp-verify'),
    path('register/cancel/', views.cancel_registration, name='register-cancel'),
]
