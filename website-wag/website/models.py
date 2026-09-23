from django.db import models
from django.http import HttpResponseRedirect

from modelcluster.fields import ParentalKey

from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Orderable, Page

from projects.models import Category

from .blocks import STANDARD_PAGE_BLOCKS


class HomePage(Page):
    template = 'site/index.html'

    hero_title = models.CharField('Titolo principale', max_length=255, blank=True, default='Per le famiglie, per il futuro — Un paese più forte insieme')
    hero_subtitle = models.TextField('Sottotitolo', blank=True, default='Sosteniamo politiche concrete per la famiglia, il lavoro e la solidarietà. Partecipa, iscriviti, dona: costruisci con noi un futuro più sicuro per i tuoi cari.')
    hero_primary_cta_text = models.CharField('Testo del pulsante arancione', max_length=100, blank=True, default='Iscriviti')
    hero_primary_cta_link = models.CharField(max_length=255, blank=True, default='/join/')
    hero_secondary_cta_text = models.CharField('Testo del pulsante bianco', max_length=100, blank=True, default='Sostienici')
    hero_secondary_cta_link = models.CharField(max_length=255, blank=True, default='/support/')

    mission_title = models.CharField('Titolo della missione', max_length=255, blank=True, default='La nostra missione')
    mission_text = models.TextField('Testo della missione', blank=True, default='Promuovere politiche che mettano al centro la famiglia, il lavoro dignitoso e la coesione sociale. Trasparenza, responsabilità e partecipazione civica guidano ogni nostra iniziativa.')

    featured_title = models.CharField('Titolo dei progetti in evidenza', max_length=255, blank=True, default='Progetti in evidenza')
    featured_text = models.TextField('Testo dei progetti in evidenza', blank=True, default='Iniziative locali e nazionali pensate per migliorare la vita quotidiana delle famiglie.')

    cta_title = models.CharField('Titolo del riquadro finale', max_length=255, blank=True, default='Sostieni il nostro lavoro')
    cta_text = models.TextField('Testo del riquadro finale', blank=True, default='Con il tuo contributo possiamo ampliare i servizi e raggiungere più famiglie. Ogni donazione conta.')

    body = RichTextField(blank=True, verbose_name='Testo')

    parent_page_types = ['wagtailcore.Page']
    subpage_types = ['website.StandardPage', 'website.ManagedSitePage']

    class Meta:
        verbose_name = 'Homepage'
        verbose_name_plural = 'Homepage'

    # hero_primary_cta_link, hero_secondary_cta_link and body are deliberately
    # left out: site/index.html never renders them (the primary button always
    # links to the join page, the secondary one is disabled), so showing them
    # here would let editors change fields with no visible effect.
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_subtitle'),
            FieldPanel('hero_primary_cta_text',
                       help_text='Il pulsante porta sempre alla pagina di iscrizione.'),
            FieldPanel('hero_secondary_cta_text',
                       help_text='Pulsante non ancora attivo (mostrato con «Prossimamente»).'),
        ], heading='Sezione iniziale'),
        MultiFieldPanel([
            FieldPanel('mission_title', heading='Titolo'),
            FieldPanel('mission_text', heading='Testo'),
        ], heading='La nostra missione'),
        InlinePanel('value_cards', label='scheda', heading='Schede della missione',
                    help_text='Se non ci sono schede, il sito mostra le 3 schede predefinite. '
                              'Appena ne aggiungi una, compaiono solo le tue.'),
        MultiFieldPanel([
            FieldPanel('featured_title', heading='Titolo'),
            FieldPanel('featured_text', heading='Testo'),
        ], heading='Progetti in evidenza'),
        InlinePanel('featured_cards', label='scheda', heading='Schede dei progetti in evidenza',
                    help_text='Se non ci sono schede, il sito mostra le 3 schede predefinite. '
                              'Appena ne aggiungi una, compaiono solo le tue.'),
        MultiFieldPanel([
            FieldPanel('cta_title', heading='Titolo'),
            FieldPanel('cta_text', heading='Testo'),
        ], heading='Riquadro finale (fascia scura)'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['cms_home'] = self
        # Login/registration moved to their own pages (members.pages.login_page/
        # join_page) — this only needs what the authenticated "Welcome back" +
        # category-grid card still shown here actually uses.
        context['categories'] = Category.objects.filter(is_active=True).order_by('order')
        return context


class HomeValueCard(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='value_cards')
    title = models.CharField('Titolo', max_length=255)
    text = models.TextField('Testo')

    panels = [
        FieldPanel('title'),
        FieldPanel('text'),
    ]


class HomeFeaturedCard(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='featured_cards')
    title = models.CharField('Titolo', max_length=255)
    text = models.TextField('Testo')

    panels = [
        FieldPanel('title'),
        FieldPanel('text'),
    ]


class StandardPage(Page):
    TEMPLATE_BY_SLUG = {
        'about': 'site/about.html',
        'projects': 'site/projects.html',
        'support': 'site/support.html',
        'contact': 'site/contact.html',
    }

    # Legacy Wagtail-page slugs that should redirect elsewhere instead of
    # rendering their own content (e.g. old bookmarks/search-index links).
    # Since the Wagtail mount moved to /sciarrone/, the old 'join' page is
    # reachable again at /sciarrone/join/ and would render as an empty
    # duplicate of the real registration page (/join/, config/urls.py).
    REDIRECT_SLUGS = {'join': '/join/'}

    def serve(self, request, *args, **kwargs):
        target = self.REDIRECT_SLUGS.get(self.slug)
        if target:
            if request.LANGUAGE_CODE == 'en':
                target = f'/en{target}'
            return HttpResponseRedirect(target)
        return super().serve(request, *args, **kwargs)

    intro = RichTextField(blank=True, features=['h2', 'h3', 'bold', 'italic', 'link'], verbose_name='Introduzione')
    body = RichTextField(blank=True, verbose_name='Testo')
    content_blocks = StreamField(STANDARD_PAGE_BLOCKS, blank=True, use_json_field=True, verbose_name='Blocchi di contenuto')

    parent_page_types = ['website.HomePage', 'website.StandardPage']
    subpage_types = ['website.StandardPage']

    class Meta:
        verbose_name = 'Pagina'
        verbose_name_plural = 'Pagine'

    content_panels = Page.content_panels + [
        FieldPanel('intro',
                   help_text='Breve testo mostrato sotto il titolo della pagina.'),
        FieldPanel('body', help_text="Testo libero, mostrato dopo l'introduzione."),
        FieldPanel('content_blocks',
                   help_text='Sezioni aggiuntive in fondo alla pagina: titoli, paragrafi, '
                             'riquadri con pulsante, schede, domande frequenti, immagini.'),
    ]

    def get_template(self, request, *args, **kwargs):
        return self.TEMPLATE_BY_SLUG.get(self.slug, 'website/standard_page.html')

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['cms_page'] = self
        if self.slug == 'contact':
            context['contact_errors'] = request.session.pop('contact_errors', None)
            context['contact_success'] = request.session.pop('contact_success', False)
        return context


class ManagedSitePage(Page):
    # Never wired up: its template reads a `managed_page` context variable
    # nothing sets, so a new instance renders blank. Hidden from "add page"
    # until it's either implemented or removed.
    is_creatable = False

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
