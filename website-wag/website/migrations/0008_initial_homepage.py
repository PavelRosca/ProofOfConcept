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

    # treebeard 4.8.0 bug: add_child() checks is_leaf() (numchild==0).
    # If we delete children first via bulk delete (which doesn't update
    # numchild), is_leaf() returns False and get_last_child() returns None,
    # causing AttributeError on ._inc_path(). Fix: add BEFORE deleting so
    # get_last_child() returns the existing "Welcome" page (non-None).
    # Use a temp slug to avoid conflict with the existing slug='home' page.
    homepage = HomePage(
        title='Home',
        slug='home-init',
        live=True,
        locale=locale_it,
    )
    root_page.add_child(instance=homepage)

    # Delete the default "Welcome to your new Wagtail site!" pages
    root_page.get_children().exclude(pk=homepage.pk).delete()
    # Bulk delete doesn't update numchild — fix it
    actual = root_page.get_children().count()
    Page.objects.filter(pk=root_page.pk).update(numchild=actual)
    # Rename to final slug now that the conflicting 'home' page is gone
    Page.objects.filter(pk=homepage.pk).update(slug='home')

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
