from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class CTASectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    text = blocks.TextBlock(required=False)
    button_text = blocks.CharBlock(required=False)
    button_url = blocks.CharBlock(required=False)
    button_style = blocks.ChoiceBlock(
        choices=[
            ('primary', 'Primary'),
            ('secondary', 'Secondary'),
            ('white', 'White'),
        ],
        default='primary',
        required=False,
    )


class CardsGridItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    text = blocks.TextBlock(required=False)
    cta_text = blocks.CharBlock(required=False)
    cta_url = blocks.CharBlock(required=False)


class CardsGridBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    columns = blocks.ChoiceBlock(
        choices=[
            ('2', '2 Columns'),
            ('3', '3 Columns'),
        ],
        default='3',
        required=False,
    )
    items = blocks.ListBlock(CardsGridItemBlock(), min_num=1)


class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(required=True)
    answer = blocks.RichTextBlock(required=True)


class FAQBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, default='Domande frequenti')
    items = blocks.ListBlock(FAQItemBlock(), min_num=1)


class ImageTextSplitBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True)
    text = blocks.RichTextBlock(required=False)
    image = ImageChooserBlock(required=True)
    image_position = blocks.ChoiceBlock(
        choices=[
            ('left', 'Image Left'),
            ('right', 'Image Right'),
        ],
        default='right',
        required=False,
    )
    cta_text = blocks.CharBlock(required=False)
    cta_url = blocks.CharBlock(required=False)


STANDARD_PAGE_BLOCKS = [
    ('heading', blocks.CharBlock(form_classname='title', icon='title')),
    ('paragraph', blocks.RichTextBlock(icon='doc-full')),
    ('cta', CTASectionBlock(icon='placeholder')),
    ('cards_grid', CardsGridBlock(icon='list-ul')),
    ('faq', FAQBlock(icon='help')),
    ('image_text_split', ImageTextSplitBlock(icon='image')),
]
