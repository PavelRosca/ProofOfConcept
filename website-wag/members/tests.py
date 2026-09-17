from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser, User
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from core import views as core_views
from core.models import Member

from . import views as members_views
from .access import is_active_member
from .models import LoginOTP, RegistrationOTP


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


@override_settings(RATELIMIT_ENABLE=False)
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
            'next': '/sciarrone/',
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


@override_settings(RATELIMIT_ENABLE=False)
class LoginRequestHoneypotTests(TestCase):
    def _payload(self, **overrides):
        payload = {'email': 'honeypot-login@example.com', 'next': '/sciarrone/'}
        payload.update(overrides)
        return payload

    def test_honeypot_filled_creates_no_otp(self):
        response = self.client.post(reverse('members:login-request'), self._payload(website='http://spam.example'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LoginOTP.objects.count(), 0)

    def test_honeypot_empty_creates_otp_normally(self):
        response = self.client.post(reverse('members:login-request'), self._payload())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(LoginOTP.objects.count(), 1)


@override_settings(RATELIMIT_ENABLE=False)
class LoginRequestAntiEnumerationTests(TestCase):
    def test_identical_response_registered_vs_unregistered(self):
        User.objects.create_user(username='member@example.com', email='member@example.com')
        response_registered = self.client.post(
            reverse('members:login-request'), {'email': 'member@example.com', 'next': '/sciarrone/'}
        )
        response_unregistered = self.client.post(
            reverse('members:login-request'), {'email': 'unregistered@example.com', 'next': '/sciarrone/'}
        )
        self.assertEqual(response_registered.status_code, response_unregistered.status_code)
        self.assertEqual(response_registered.url, response_unregistered.url)

    def test_email_content_differs_by_account_existence(self):
        User.objects.create_user(username='member2@example.com', email='member2@example.com')
        self.client.post(reverse('members:login-request'), {'email': 'member2@example.com', 'next': '/sciarrone/'})
        self.client.post(reverse('members:login-request'), {'email': 'ghost@example.com', 'next': '/sciarrone/'})
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn('accesso', mail.outbox[0].subject.lower())
        self.assertIn('nessun account', mail.outbox[1].subject.lower())


@override_settings(RATELIMIT_ENABLE=False)
class LoginVerifyTests(TestCase):
    def _make_pending_otp(self, email, code='123456', **overrides):
        now = timezone.now()
        defaults = dict(
            email=email,
            otp_hash=make_password(code),
            expires_at=now + timedelta(minutes=10),
            last_sent_at=now,
        )
        defaults.update(overrides)
        return LoginOTP.objects.create(**defaults)

    def _set_pending(self, otp_id):
        session = self.client.session
        session['pending_login_id'] = otp_id
        session.save()

    def test_correct_code_logs_in_existing_user(self):
        user = User.objects.create_user(username='login-ok@example.com', email='login-ok@example.com')
        otp = self._make_pending_otp('login-ok@example.com')
        self._set_pending(otp.pk)
        response = self.client.post(reverse('members:login-verify'), {'code': '123456', 'next': '/sciarrone/'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_wrong_code_increments_attempts_and_does_not_log_in(self):
        User.objects.create_user(username='login-wrong@example.com', email='login-wrong@example.com')
        otp = self._make_pending_otp('login-wrong@example.com')
        self._set_pending(otp.pk)
        response = self.client.post(reverse('members:login-verify'), {'code': '000000', 'next': '/sciarrone/'})
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)
        otp.refresh_from_db()
        self.assertEqual(otp.attempts, 1)

    def test_expired_code_fails_generically(self):
        User.objects.create_user(username='login-exp@example.com', email='login-exp@example.com')
        otp = self._make_pending_otp('login-exp@example.com', expires_at=timezone.now() - timedelta(minutes=1))
        self._set_pending(otp.pk)
        response = self.client.post(reverse('members:login-verify'), {'code': '123456', 'next': '/sciarrone/'})
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_account_missing_between_request_and_verify_fails_generically(self):
        # No matching User at all — simulates the account being deleted after
        # the code was requested.
        otp = self._make_pending_otp('login-ghost@example.com')
        self._set_pending(otp.pk)
        response = self.client.post(reverse('members:login-verify'), {'code': '123456', 'next': '/sciarrone/'})
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_inactive_user_fails_generically(self):
        User.objects.create_user(
            username='login-inactive@example.com', email='login-inactive@example.com', is_active=False
        )
        otp = self._make_pending_otp('login-inactive@example.com')
        self._set_pending(otp.pk)
        response = self.client.post(reverse('members:login-verify'), {'code': '123456', 'next': '/sciarrone/'})
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)


class LogoutTests(TestCase):
    def test_get_not_allowed(self):
        response = self.client.get(reverse('members:logout'))
        self.assertEqual(response.status_code, 405)

    def test_post_logs_out_and_clears_session(self):
        user = User.objects.create_user(username='logout-me@example.com', email='logout-me@example.com')
        self.client.force_login(user)
        response = self.client.post(reverse('members:logout'), {'next': '/sciarrone/'})
        self.assertEqual(response.status_code, 302)
        self.assertNotIn('_auth_user_id', self.client.session)


class LoginJoinPageTests(TestCase):
    def test_login_page_anonymous_renders_form(self):
        response = self.client.get(reverse('login-page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id_login_email')

    def test_join_page_anonymous_renders_form(self):
        response = self.client.get(reverse('join-page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id_first_name')

    def test_login_page_authenticated_redirects_home(self):
        user = User.objects.create_user(username='pageuser@example.com', email='pageuser@example.com')
        self.client.force_login(user)
        response = self.client.get(reverse('login-page'))
        self.assertRedirects(response, '/sciarrone/', fetch_redirect_response=False)

    def test_join_page_authenticated_redirects_home(self):
        user = User.objects.create_user(username='pageuser2@example.com', email='pageuser2@example.com')
        self.client.force_login(user)
        response = self.client.get(reverse('join-page'))
        self.assertRedirects(response, '/sciarrone/', fetch_redirect_response=False)

    def test_login_page_pending_shows_otp_step(self):
        session = self.client.session
        session['pending_login_id'] = 1
        session.save()
        response = self.client.get(reverse('login-page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id_login_code')

    def test_login_page_english_renders_english_copy(self):
        response = self.client.get('/en/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Log in')


@override_settings(RATELIMIT_ENABLE=True)
class RateLimitInlineNoticeTests(TestCase):
    """Exceeding any of these views' rate limit must redirect back with a
    session-flash notice (block=False), never raise django_ratelimit's
    Ratelimited (which would otherwise render templates/403.html on its
    own, separate page — see the 2026-09-10 UX pass)."""

    def _hammer(self, url, payload, times):
        response = None
        for _ in range(times):
            response = self.client.post(url, payload)
            self.assertEqual(response.status_code, 302, 'rate-limited requests must still redirect, never 403')
        return response

    def test_register_submit_rate_limited_inline(self):
        self._hammer(reverse('members:register-submit'), {'next': '/sciarrone/'}, 8)
        self.assertEqual(
            self.client.session.get('registration_errors'), {'__all__': [members_views.RATE_LIMIT_ERROR]}
        )

    def test_resend_otp_rate_limited_inline(self):
        self._hammer(reverse('members:otp-resend'), {'next': '/sciarrone/'}, 6)
        self.assertEqual(self.client.session.get('otp_errors'), [members_views.RATE_LIMIT_ERROR])

    def test_verify_otp_rate_limited_inline(self):
        # No pending_registration_id set — pending_registration_key() then
        # keys on the shared 'anon' bucket, so the 8/10m per-pending-id limit
        # (not the 15/h per-IP one) is the one that trips first.
        self._hammer(reverse('members:otp-verify'), {'code': '000000', 'next': '/sciarrone/'}, 11)
        self.assertEqual(self.client.session.get('otp_errors'), [members_views.RATE_LIMIT_ERROR])

    def test_login_request_rate_limited_inline(self):
        self._hammer(reverse('members:login-request'), {'email': 'ratelimit@example.com', 'next': '/sciarrone/'}, 8)
        self.assertEqual(self.client.session.get('login_errors'), {'__all__': [members_views.RATE_LIMIT_ERROR]})

    def test_login_resend_rate_limited_inline(self):
        self._hammer(reverse('members:login-resend'), {'next': '/sciarrone/'}, 6)
        self.assertEqual(self.client.session.get('login_otp_errors'), [members_views.RATE_LIMIT_ERROR])

    def test_login_verify_rate_limited_inline(self):
        self._hammer(reverse('members:login-verify'), {'code': '000000', 'next': '/sciarrone/'}, 11)
        self.assertEqual(self.client.session.get('login_otp_errors'), [members_views.RATE_LIMIT_ERROR])

    def test_contact_submit_rate_limited_inline(self):
        self._hammer(reverse('contact-submit'), {'next': '/sciarrone/'}, 13)
        self.assertEqual(
            self.client.session.get('contact_errors'), {'__all__': [core_views.CONTACT_RATE_LIMIT_ERROR]}
        )
