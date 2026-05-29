from django.db import migrations


def create_initial_homepage(apps, schema_editor):
    from wagtail.models import Locale, Page, Site
    from website.models import HomePage

    if HomePage.objects.exists():
        return

    locale_it, _ = Locale.objects.get_or_create(language_code='it')

    root_page = Page.objects.filter(depth=1).first()
    if not root_page:
        return

    root_page.get_children().delete()

    homepage = HomePage(
        title='Home',
        slug='home',
        live=True,
        locale=locale_it,
    )
    root_page.add_child(instance=homepage)

    site = Site.objects.filter(is_default_site=True).first()
    if site:
        site.root_page = homepage
        site.save()
    else:
        Site.objects.create(
            hostname='localhost',
            port=80,
            root_page=homepage,
            is_default_site=True,
            site_name='Partito CMS',
        )


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_remove_standardpage_layout_preset_and_more'),
        ('wagtailcore', '0096_referenceindex_referenceindex_source_object_and_more'),
    ]

    operations = [
        migrations.RunPython(create_initial_homepage, migrations.RunPython.noop),
    ]
