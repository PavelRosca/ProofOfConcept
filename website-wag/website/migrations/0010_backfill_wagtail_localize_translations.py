from django.db import migrations


def backfill_translations(apps, schema_editor):
    """Registers the existing IT->EN page pairs (created directly via migration
    0009, not through wagtail-localize's own "Translate this page" flow) with
    wagtail-localize's own TranslationSource/Translation bookkeeping tables, so
    its "Sync" action appears in the Wagtail admin Actions menu.

    Only creates wagtail-localize's tracking rows from a snapshot of the IT
    page's current content — never touches the existing IT or EN page content
    itself (deliberately avoids TranslationCreator/save_target, which would
    overwrite the EN pages' already-translated fields with IT fallback text).
    """
    from wagtail.models import Locale
    from wagtail_localize.models import Translation, TranslationSource
    from website.models import HomePage, StandardPage

    locale_it = Locale.objects.filter(language_code='it').first()
    locale_en = Locale.objects.filter(language_code='en').first()
    if not locale_it or not locale_en:
        return

    it_pages = list(HomePage.objects.filter(locale=locale_it)) + list(
        StandardPage.objects.filter(locale=locale_it)
    )

    for it_page in it_pages:
        if not StandardPage.objects.filter(
            locale=locale_en, translation_key=it_page.translation_key
        ).exists() and not HomePage.objects.filter(
            locale=locale_en, translation_key=it_page.translation_key
        ).exists():
            continue

        source, _ = TranslationSource.get_or_create_from_instance(it_page)
        Translation.objects.get_or_create(
            source=source,
            target_locale=locale_en,
            defaults={'enabled': True},
        )


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_create_en_locale_and_pages'),
        ('wagtail_localize', '0016_rename_page_revision_translationlog_revision'),
        ('wagtailcore', '0096_referenceindex_referenceindex_source_object_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_translations, migrations.RunPython.noop),
    ]
