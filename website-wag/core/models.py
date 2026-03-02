from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.utils import timezone


class Sector(models.Model):
    """Political party sectors/regions"""
    REGION_TYPES = [
        ('nord', 'Nord (Northern)'),
        ('centro', 'Centro (Central)'),
        ('sud', 'Sud/Isole (South/Islands)'),
    ]
    
    name = models.CharField(max_length=100)
    region_type = models.CharField(max_length=10, choices=REGION_TYPES)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['region_type', 'order']
        verbose_name_plural = 'Sectors'
        
    def __str__(self):
        return f"{self.name} ({self.get_region_type_display()})"


class Region(models.Model):
    """Regions within sectors"""
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE, related_name='regions')
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)  # e.g., NORD-01
    description = models.TextField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sector', 'name']
        unique_together = ['sector', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.code})"


class Project(models.Model):
    """Political party projects"""
    STATUS_CHOICES = [
        ('planificato', 'Planificato'),
        ('in_corso', 'In Corso'),
        ('completato', 'Completato'),
        ('sospeso', 'Sospeso'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planificato')
    sectors = models.ManyToManyField(Sector, related_name='projects')
    budget = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    order = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title


class Member(models.Model):
    """Political party members"""
    MEMBERSHIP_STATUS = [
        ('attivo', 'Attivo'),
        ('inattivo', 'Inattivo'),
        ('sospeso', 'Sospeso'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member')
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')
    tessera_number = models.CharField(max_length=50, unique=True, blank=True, null=True)  # Membership card
    status = models.CharField(max_length=20, choices=MEMBERSHIP_STATUS, default='attivo')
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_joined']
        
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.tessera_number})"


class Donation(models.Model):
    """Donations to the party"""
    DONATION_STATUS = [
        ('pending', 'In Sospeso'),
        ('completed', 'Completato'),
        ('failed', 'Fallito'),
        ('refunded', 'Rimborsato'),
    ]
    
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20, blank=True, null=True)
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EUR')
    status = models.CharField(max_length=20, choices=DONATION_STATUS, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)  # e.g., stripe, paypal, bank_transfer
    transaction_id = models.CharField(max_length=200, blank=True, null=True, unique=True)
    message = models.TextField(blank=True, null=True)
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Donation {self.amount} EUR - {self.donor_name} ({self.status})"


class StaticPage(models.Model):
    """Static pages like Statute, Privacy, etc."""
    PAGES = [
        ('statuto', 'Statuto'),
        ('privacy', 'Privacy / Confidenza'),
        ('garantia', 'Commissione di Garanzia'),
        ('bilanci', 'Bilanci'),
        ('contributi', 'Contributi Ricevuti'),
        ('regolamento_adezioni', 'Regolamento Adesioni'),
        ('regolamento_congressi', 'Regolamento Congressi'),
        ('contatti', 'Contatti'),
    ]
    
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200)
    page_type = models.CharField(max_length=50, choices=PAGES)
    content = models.TextField()
    order = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Static Pages'
        
    def __str__(self):
        return self.title
