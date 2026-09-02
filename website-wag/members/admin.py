from django.contrib import admin

from .models import RegistrationOTP


@admin.register(RegistrationOTP)
class RegistrationOTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'expires_at', 'verified_at', 'attempts', 'resend_count')
    list_filter = ('verified_at', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('created_at',)
    exclude = ('otp_hash',)
