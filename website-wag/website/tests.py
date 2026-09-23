from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from core.models import Member
from projects.models import Category


class HomepageCategoryGridTests(TestCase):
    def _make_member(self, username, status='attivo'):
        user = User.objects.create_user(username=username, email=username)
        Member.objects.create(user=user, status=status)
        return user

    def test_anonymous_visitor_sees_no_grid(self):
        response = self.client.get('/sciarrone/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Agricoltura')

    def test_active_member_sees_grid_with_all_categories(self):
        user = self._make_member('gridactive@example.com')
        self.client.force_login(user)
        response = self.client.get('/sciarrone/')
        self.assertEqual(response.status_code, 200)
        for category in Category.objects.filter(is_active=True):
            url = reverse('projects:category-detail', kwargs={'key': category.key})
            self.assertContains(response, url)

    def test_inactive_member_sees_welcome_but_no_grid(self):
        user = self._make_member('gridinactive@example.com', status='inattivo')
        self.client.force_login(user)
        response = self.client.get('/sciarrone/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Benvenuto')
        self.assertNotContains(response, 'Agricoltura')

    def test_user_without_member_no_crash(self):
        user = User.objects.create_superuser(username='gridadmin@example.com', email='gridadmin@example.com', password='irrelevant')
        self.client.force_login(user)
        response = self.client.get('/sciarrone/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Agricoltura')


class StandardPageCmsContentTests(TestCase):
    """Every field shown in a StandardPage's CMS edit form must actually reach
    the rendered page (body used to be silently dropped by site/*.html)."""

    def _live_page(self, slug):
        from website.models import StandardPage
        page = StandardPage.objects.live().filter(slug=slug, locale__language_code='it').first()
        self.assertIsNotNone(page, f'no live IT StandardPage with slug {slug!r}')
        return page

    def test_body_is_rendered_on_fixed_template_pages(self):
        for slug in ('about', 'projects', 'support', 'contact'):
            page = self._live_page(slug)
            page.body = f'<p>Testo di prova {slug}</p>'
            page.save_revision().publish()
            response = self.client.get(page.get_url())
            self.assertContains(response, f'Testo di prova {slug}', msg_prefix=slug)

    def test_legacy_join_page_redirects_to_registration(self):
        response = self.client.get('/sciarrone/join/')
        self.assertRedirects(response, '/join/', fetch_redirect_response=False)

    def test_image_text_split_block_renders_real_image(self):
        import shutil
        import tempfile
        from io import BytesIO

        from django.core.files.images import ImageFile
        from django.test import override_settings
        from PIL import Image as PILImage
        from wagtail.images.models import Image

        media_root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, media_root, ignore_errors=True)
        with override_settings(MEDIA_ROOT=media_root):
            buf = BytesIO()
            PILImage.new('RGB', (40, 30), 'orange').save(buf, 'PNG')
            image = Image.objects.create(title='Prova', file=ImageFile(buf, name='prova.png'))
            page = self._live_page('about')
            page.content_blocks = [('image_text_split', {
                'title': 'Insieme sul territorio', 'text': '', 'image': image,
                'image_position': 'right', 'cta_text': '', 'cta_url': '',
            })]
            page.save_revision().publish()
            response = self.client.get(page.get_url())
        self.assertContains(response, 'Insieme sul territorio')
        self.assertNotContains(response, 'src=""')
        self.assertContains(response, 'alt="Insieme sul territorio"')
