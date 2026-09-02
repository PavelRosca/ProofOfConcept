import secrets
from datetime import timedelta

from django.db import models

OTP_LENGTH = 6
OTP_TTL = timedelta(minutes=10)
RESEND_COOLDOWN = timedelta(seconds=60)
MAX_OTP_ATTEMPTS = 5
MAX_RESENDS = 5


def generate_otp():
    """Cryptographically secure zero-padded 6-digit numeric code."""
    return f'{secrets.randbelow(10 ** OTP_LENGTH):0{OTP_LENGTH}d}'


class RegistrationOTP(models.Model):
    """Pending, unverified homepage registration. Promoted to User+Member on OTP verification."""

    email = models.EmailField(db_index=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    address_street = models.CharField(max_length=200)
    address_number = models.CharField(max_length=20)
    address_postal_code = models.CharField(max_length=10)
    address_city = models.CharField(max_length=100)
    address_province = models.CharField(max_length=2)

    otp_hash = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    last_sent_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    resend_count = models.PositiveSmallIntegerField(default=0)
    verified_at = models.DateTimeField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} ({'verified' if self.verified_at else 'pending'})"
