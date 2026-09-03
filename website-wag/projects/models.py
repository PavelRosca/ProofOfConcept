from django.db import models


class Category(models.Model):
    """One of the six fixed thematic categories shown to authenticated, active
    members after registration (Phase 3). Labels are fixed and not CMS-editable,
    so they live in LABELS rather than as extra bilingual DB columns. Real
    per-category content (the questionnaire) is Phase 4 — this model is
    deliberately minimal."""

    LABELS = {
        'agricoltura': ('Agricoltura', 'Agriculture'),
        'ambiente': ('Ambiente', 'Environment'),
        'finanza': ('Finanza', 'Finance'),
        'giustizia': ('Giustizia', 'Justice'),
        'imprese': ('Imprese', 'Businesses'),
        'istituzioni': ('Istituzioni', 'Institutions'),
    }

    key = models.SlugField(max_length=50, unique=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'key']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.key

    @property
    def label_it(self):
        return self.LABELS.get(self.key, (self.key.title(), self.key.title()))[0]

    @property
    def label_en(self):
        return self.LABELS.get(self.key, (self.key.title(), self.key.title()))[1]
