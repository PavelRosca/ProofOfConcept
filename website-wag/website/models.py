from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page

from .blocks import STANDARD_PAGE_BLOCKS


class HomePage(Page):
    template = 'site/index.html'

    hero_title = models.CharField(max_length=255, blank=True, default='Per le famiglie, per il futuro — Un paese più forte insieme')
    hero_subtitle = models.TextField(blank=True, default='Sosteniamo politiche concrete per la famiglia, il lavoro e la solidarietà. Partecipa, iscriviti, dona: costruisci con noi un futuro più sicuro per i tuoi cari.')
    hero_primary_cta_text = models.CharField(max_length=100, blank=True, default='Iscriviti')
    hero_primary_cta_link = models.CharField(max_length=255, blank=True, default='/join/')
    hero_secondary_cta_text = models.CharField(max_length=100, blank=True, default='Sostienici')
    hero_secondary_cta_link = models.CharField(max_length=255, blank=True, default='/support/')

    mission_title = models.CharField(max_length=255, blank=True, default='La nostra missione')
    mission_text = models.TextField(blank=True, default='Promuovere politiche che mettano al centro la famiglia, il lavoro dignitoso e la coesione sociale. Trasparenza, responsabilità e partecipazione civica guidano ogni nostra iniziativa.')

    featured_title = models.CharField(max_length=255, blank=True, default='Progetti in evidenza')
    featured_text = models.TextField(blank=True, default='Iniziative locali e nazionali pensate per migliorare la vita quotidiana delle famiglie.')

    cta_title = models.CharField(max_length=255, blank=True, default='Sostieni il nostro lavoro')
    cta_text = models.TextField(blank=True, default='Con il tuo contributo possiamo ampliare i servizi e raggiungere più famiglie. Ogni donazione conta.')

    body = RichTextField(blank=True)

    parent_page_types = ['wagtailcore.Page']
    subpage_types = ['website.StandardPage', 'website.ManagedSitePage']

    content_panels = Page.content_panels + [
        FieldPanel('hero_title'),
        FieldPanel('hero_subtitle'),
        FieldPanel('hero_primary_cta_text'),
        FieldPanel('hero_primary_cta_link'),
        FieldPanel('hero_secondary_cta_text'),
        FieldPanel('hero_secondary_cta_link'),
        FieldPanel('mission_title'),
        FieldPanel('mission_text'),
        InlinePanel('value_cards', label='Mission Value Cards'),
        FieldPanel('featured_title'),
        FieldPanel('featured_text'),
        InlinePanel('featured_cards', label='Featured Project Cards'),
        FieldPanel('cta_title'),
        FieldPanel('cta_text'),
        FieldPanel('body'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['cms_home'] = self
        return context


class HomeValueCard(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='value_cards')
    title = models.CharField(max_length=255)
    text = models.TextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('text'),
    ]


class HomeFeaturedCard(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='featured_cards')
    title = models.CharField(max_length=255)
    text = models.TextField()

    panels = [
        FieldPanel('title'),
        FieldPanel('text'),
    ]


class StandardPage(Page):
    TEMPLATE_BY_SLUG = {
        'about': 'site/about.html',
        'projects': 'site/projects.html',
        'support': 'site/support.html',
        'join': 'site/join.html',
        'contact': 'site/contact.html',
    }

    intro = RichTextField(blank=True, features=['h2', 'h3', 'bold', 'italic', 'link'])
    body = RichTextField(blank=True)
    content_blocks = StreamField(STANDARD_PAGE_BLOCKS, blank=True, use_json_field=True)

    parent_page_types = ['website.HomePage', 'website.StandardPage']
    subpage_types = ['website.StandardPage']

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('content_blocks'),
    ]

    def get_template(self, request, *args, **kwargs):
        return self.TEMPLATE_BY_SLUG.get(self.slug, 'website/standard_page.html')

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['cms_page'] = self
        return context


class ManagedSitePage(Page):
    target_slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text='Slug-ul rutei existente, ex: index, about, projects',
    )
    html_content = models.TextField(
        blank=True,
        help_text='Conținut HTML complet pentru pagina target. Dacă este gol, se folosește fallback-ul static.',
    )

    parent_page_types = ['website.HomePage', 'wagtailcore.Page']
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel('target_slug'),
        FieldPanel('html_content'),
    ]
