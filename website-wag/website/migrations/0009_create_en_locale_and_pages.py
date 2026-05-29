import uuid
from django.db import migrations


def _safe_add_child(parent, instance):
    """Workaround for treebeard 4.8.0 bug: add_child() crashes when the parent
    has no children because it calls get_last_child()._inc_path() without a
    None check. Fall back to manual path calculation for the first child."""
    from django.db.models import F
    try:
        parent.add_child(instance=instance)
    except AttributeError:
        steplen = type(parent).steplen
        instance.path = parent.path + '1'.rjust(steplen, '0')
        instance.depth = parent.depth + 1
        instance.numchild = 0
        instance.save()
        type(parent).objects.filter(pk=parent.pk).update(numchild=F('numchild') + 1)


IT_SUBPAGES = [
    ('about',    'Informazioni'),
    ('projects', 'Progetti'),
    ('support',  'Assistenza'),
    ('join',     'Unisciti'),
    ('contact',  'Contatto'),
]

EN_SUBPAGES = [
    ('about',    'About'),
    ('projects', 'Projects'),
    ('support',  'Support'),
    ('join',     'Join'),
    ('contact',  'Contact'),
]


def create_en_locale_and_pages(apps, schema_editor):
    from wagtail.models import Locale, Page
    from website.models import HomePage, StandardPage

    locale_it = Locale.objects.filter(language_code='it').first()
    if not locale_it:
        return

    locale_en, _ = Locale.objects.get_or_create(language_code='en')

    homepage_it = HomePage.objects.filter(locale=locale_it).first()
    if not homepage_it:
        return

    root_page = Page.objects.get(depth=1)

    # Create EN homepage as a translation of the IT homepage
    if not HomePage.objects.filter(locale=locale_en).exists():
        homepage_en = HomePage(
            title='Home',
            slug='home-en',
            live=True,
            locale=locale_en,
            translation_key=homepage_it.translation_key,
            hero_title='For families, for the future — A stronger country together',
            hero_subtitle=(
                'We support concrete policies for family, work, and solidarity. '
                'Take part, join, donate: build with us a safer future for your loved ones.'
            ),
            hero_primary_cta_text='Sign up',
            hero_primary_cta_link='/en/join/',
            hero_secondary_cta_text='Support us',
            hero_secondary_cta_link='/en/support/',
            mission_title='Our mission',
            mission_text=(
                'Promote policies that put family, decent work, and social cohesion at the center. '
                'Transparency, accountability, and civic participation guide every initiative we undertake.'
            ),
            featured_title='Featured projects',
            featured_text='Local and national initiatives designed to improve the daily lives of families.',
            cta_title='Support our work',
            cta_text=(
                'With your contribution, we can expand services and reach more families. '
                'Every donation counts.'
            ),
        )
        root_page.add_child(instance=homepage_en)
    else:
        homepage_en = HomePage.objects.filter(locale=locale_en).first()

    # Create IT subpages if none exist yet
    if not StandardPage.objects.filter(locale=locale_it).exists():
        for slug, title in IT_SUBPAGES:
            sp = StandardPage(title=title, slug=slug, live=True, locale=locale_it)
            _safe_add_child(homepage_it, sp)

    # Create EN subpages as translations of IT subpages
    if not StandardPage.objects.filter(locale=locale_en).exists():
        it_pages = {sp.slug: sp for sp in StandardPage.objects.filter(locale=locale_it)}
        for slug, title in EN_SUBPAGES:
            it_page = it_pages.get(slug)
            translation_key = it_page.translation_key if it_page else uuid.uuid4()
            sp = StandardPage(
                title=title,
                slug=slug,
                live=True,
                locale=locale_en,
                translation_key=translation_key,
            )
            _safe_add_child(homepage_en, sp)


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_initial_homepage'),
        ('wagtailcore', '0096_referenceindex_referenceindex_source_object_and_more'),
    ]

    operations = [
        migrations.RunPython(create_en_locale_and_pages, migrations.RunPython.noop),
    ]
