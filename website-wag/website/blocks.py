from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

# Labels are Italian to match the rest of the (Italian) Wagtail admin. Link
# help text spells out the /sciarrone/ and /en/ prefixes because link fields
# are plain text, not page choosers.
LINK_HELP = ('Es. /join/ (iscrizione), /sciarrone/contact/ (contatti) o un indirizzo completo https://… '
             'Sulle pagine in inglese aggiungi /en davanti: /en/join/, /en/sciarrone/contact/.')


class CTASectionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, label='Titolo')
    text = blocks.TextBlock(required=False, label='Testo')
    button_text = blocks.CharBlock(required=False, label='Testo del pulsante')
    button_url = blocks.CharBlock(required=False, label='Link del pulsante', help_text=LINK_HELP)
    button_style = blocks.ChoiceBlock(
        choices=[
            ('primary', 'Arancione'),
            ('secondary', 'Solo contorno'),
            ('white', 'Solo contorno (chiaro)'),
        ],
        default='primary',
        required=False,
        label='Stile del pulsante',
    )


class CardsGridItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, label='Titolo')
    text = blocks.TextBlock(required=False, label='Testo')
    cta_text = blocks.CharBlock(required=False, label='Testo del link')
    cta_url = blocks.CharBlock(required=False, label='Link', help_text=LINK_HELP)


class CardsGridBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, label='Titolo della sezione')
    columns = blocks.ChoiceBlock(
        choices=[
            ('2', '2 colonne'),
            ('3', '3 colonne'),
        ],
        default='3',
        required=False,
        label='Colonne',
    )
    items = blocks.ListBlock(CardsGridItemBlock(label='Scheda'), min_num=1, label='Schede')


class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(required=True, label='Domanda')
    answer = blocks.RichTextBlock(required=True, label='Risposta')


class FAQBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, default='Domande frequenti', label='Titolo della sezione')
    items = blocks.ListBlock(FAQItemBlock(label='Domanda'), min_num=1, label='Domande')


class ImageTextSplitBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, label='Titolo')
    text = blocks.RichTextBlock(required=False, label='Testo')
    image = ImageChooserBlock(required=True, label='Immagine')
    image_position = blocks.ChoiceBlock(
        choices=[
            ('left', 'Immagine a sinistra'),
            ('right', 'Immagine a destra'),
        ],
        default='right',
        required=False,
        label="Posizione dell'immagine",
    )
    cta_text = blocks.CharBlock(required=False, label='Testo del pulsante')
    cta_url = blocks.CharBlock(required=False, label='Link del pulsante', help_text=LINK_HELP)


STANDARD_PAGE_BLOCKS = [
    ('heading', blocks.CharBlock(form_classname='title', icon='title', label='Titolo')),
    ('paragraph', blocks.RichTextBlock(icon='doc-full', label='Paragrafo')),
    ('cta', CTASectionBlock(icon='placeholder', label='Riquadro con pulsante')),
    ('cards_grid', CardsGridBlock(icon='list-ul', label='Griglia di schede')),
    ('faq', FAQBlock(icon='help', label='Domande frequenti')),
    ('image_text_split', ImageTextSplitBlock(icon='image', label='Immagine e testo')),
]
