from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase
from django.urls import reverse

from core.models import Member

from .access import is_active_member
from .models import RegistrationOTP


class IsActiveMemberTests(TestCase):
    def test_anonymous_user_is_not_active_member(self):
        self.assertFalse(is_active_member(AnonymousUser()))

    def test_active_member_is_active(self):
        user = User.objects.create_user(username='attivo@example.com', email='attivo@example.com')
        Member.objects.create(user=user, status='attivo')
        self.assertTrue(is_active_member(user))

    def test_inactive_member_is_not_active(self):
        user = User.objects.create_user(username='inattivo@example.com', email='inattivo@example.com')
        Member.objects.create(user=user, status='inattivo')
        self.assertFalse(is_active_member(user))

    def test_suspended_member_is_not_active(self):
        user = User.objects.create_user(username='sospeso@example.com', email='sospeso@example.com')
        Member.objects.create(user=user, status='sospeso')
        self.assertFalse(is_active_member(user))

    def test_user_without_member_is_not_active(self):
        user = User.objects.create_superuser(username='admin@example.com', email='admin@example.com', password='irrelevant')
        self.assertFalse(is_active_member(user))


class RegisterSubmitHoneypotTests(TestCase):
    def _payload(self, **overrides):
        payload = {
            'first_name': 'Mario',
            'last_name': 'Rossi',
            'email': 'honeypot-test@example.com',
            'phone': '3331234567',
            'address_street': 'Via Roma',
            'address_number': '1',
            'address_postal_code': '00100',
            'address_city': 'Roma',
            'address_province': 'RM',
            'next': '/',
        }
        payload.update(overrides)
        return payload

    def test_honeypot_filled_creates_no_otp(self):
        response = self.client.post(reverse('members:register-submit'), self._payload(website='http://spam.example'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RegistrationOTP.objects.count(), 0)

    def test_honeypot_empty_creates_otp_normally(self):
        response = self.client.post(reverse('members:register-submit'), self._payload())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(RegistrationOTP.objects.count(), 1)
