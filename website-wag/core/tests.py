from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactLead


@override_settings(RATELIMIT_ENABLE=False)
class ContactSubmitHoneypotTests(TestCase):
    def test_honeypot_filled_creates_no_lead(self):
        response = self.client.post(reverse('contact-submit'), {
            'email': 'honeypot-contact@example.com',
            'website': 'http://spam.example',
            'next': '/contact/',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactLead.objects.count(), 0)

    def test_honeypot_empty_creates_lead_normally(self):
        response = self.client.post(reverse('contact-submit'), {
            'email': 'real-contact@example.com',
            'next': '/contact/',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ContactLead.objects.count(), 1)
