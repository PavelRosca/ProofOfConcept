from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import Member

from .models import Category


class CategoryModelTests(TestCase):
    def test_str_returns_key(self):
        category = Category(key='agricoltura')
        self.assertEqual(str(category), 'agricoltura')

    def test_migration_seeded_six_categories(self):
        self.assertEqual(Category.objects.count(), 6)
        for key in ['agricoltura', 'ambiente', 'finanza', 'giustizia', 'imprese', 'istituzioni']:
            self.assertTrue(Category.objects.filter(key=key).exists())


class CategoryDetailViewTests(TestCase):
    def _make_member(self, username, status='attivo'):
        user = User.objects.create_user(username=username, email=username)
        Member.objects.create(user=user, status=status)
        return user

    def test_anonymous_redirected_to_home(self):
        response = self.client.get(reverse('projects:category-detail', kwargs={'key': 'agricoltura'}))
        self.assertRedirects(response, '/', fetch_redirect_response=False)

    def test_suspended_member_redirected_to_home(self):
        user = self._make_member('sospeso@example.com', status='sospeso')
        self.client.force_login(user)
        response = self.client.get(reverse('projects:category-detail', kwargs={'key': 'agricoltura'}))
        self.assertRedirects(response, '/', fetch_redirect_response=False)

    def test_active_member_sees_category_page(self):
        user = self._make_member('attivo@example.com')
        self.client.force_login(user)
        response = self.client.get(reverse('projects:category-detail', kwargs={'key': 'agricoltura'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Agricoltura')

    def test_unknown_key_is_404(self):
        user = self._make_member('attivo2@example.com')
        self.client.force_login(user)
        response = self.client.get(reverse('projects:category-detail', kwargs={'key': 'doesnotexist'}))
        self.assertEqual(response.status_code, 404)

    def test_inactive_category_is_404(self):
        Category.objects.filter(key='ambiente').update(is_active=False)
        user = self._make_member('attivo3@example.com')
        self.client.force_login(user)
        response = self.client.get(reverse('projects:category-detail', kwargs={'key': 'ambiente'}))
        self.assertEqual(response.status_code, 404)

    def test_user_without_member_redirected_not_crashed(self):
        user = User.objects.create_superuser(username='admin2@example.com', email='admin2@example.com', password='irrelevant')
        self.client.force_login(user)
        response = self.client.get(reverse('projects:category-detail', kwargs={'key': 'agricoltura'}))
        self.assertRedirects(response, '/', fetch_redirect_response=False)
