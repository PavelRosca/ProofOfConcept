from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse

from core.models import Member
from projects.models import Category

from website.models import StandardPage


class HomepageCategoryGridTests(TestCase):
    def _make_member(self, username, status='attivo'):
        user = User.objects.create_user(username=username, email=username)
        Member.objects.create(user=user, status=status)
        return user

    def test_anonymous_visitor_sees_no_grid(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Agricoltura')

    def test_active_member_sees_grid_with_all_categories(self):
        user = self._make_member('gridactive@example.com')
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        for category in Category.objects.filter(is_active=True):
            url = reverse('projects:category-detail', kwargs={'key': category.key})
            self.assertContains(response, url)

    def test_inactive_member_sees_welcome_but_no_grid(self):
        user = self._make_member('gridinactive@example.com', status='inattivo')
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Benvenuto')
        self.assertNotContains(response, 'Agricoltura')

    def test_user_without_member_no_crash(self):
        user = User.objects.create_superuser(username='gridadmin@example.com', email='gridadmin@example.com', password='irrelevant')
        self.client.force_login(user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Agricoltura')


class JoinRedirectTests(TestCase):
    """Registration moved to the homepage — /join/ is kept alive only as a
    redirect for old bookmarks/search-index links, not a real page."""

    def _serve(self, language_code):
        request = RequestFactory().get('/join/')
        request.LANGUAGE_CODE = language_code
        return StandardPage(slug='join').serve(request)

    def test_join_redirects_to_registration_it(self):
        response = self._serve('it')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/#registration')

    def test_join_redirects_to_registration_en(self):
        response = self._serve('en')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/en/#registration')
