from django.db import migrations

CATEGORY_KEYS = [
    'agricoltura',
    'ambiente',
    'finanza',
    'giustizia',
    'imprese',
    'istituzioni',
]


def seed_categories(apps, schema_editor):
    Category = apps.get_model('projects', 'Category')
    for order, key in enumerate(CATEGORY_KEYS):
        Category.objects.get_or_create(key=key, defaults={'order': order})


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_categories, migrations.RunPython.noop),
    ]
