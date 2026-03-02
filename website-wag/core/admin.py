from django.contrib import admin
from .models import Sector, Region, Project, Member, Donation, StaticPage


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'region_type', 'order', 'created_at')
    list_filter = ('region_type', 'created_at')
    search_fields = ('name', 'description')
    ordering = ('region_type', 'order')


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'sector', 'active', 'contact_email')
    list_filter = ('sector', 'active', 'created_at')
    search_fields = ('name', 'code', 'contact_email')
    fieldsets = (
        ('Basic Information', {
            'fields': ('sector', 'name', 'code', 'description')
        }),
        ('Contact', {
            'fields': ('contact_email', 'contact_phone')
        }),
        ('Status', {
            'fields': ('active',)
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'start_date', 'budget', 'is_featured')
    list_filter = ('status', 'is_featured', 'created_at', 'sectors')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('sectors',)
    fieldsets = (
        ('Project Info', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Timeline & Budget', {
            'fields': ('start_date', 'end_date', 'budget')
        }),
        ('Organization', {
            'fields': ('sectors', 'status', 'order', 'is_featured', 'image')
        }),
    )


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'tessera_number', 'region', 'status', 'date_joined')
    list_filter = ('status', 'region', 'date_joined')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'tessera_number')
    readonly_fields = ('date_joined', 'last_updated')
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'profile_image')
        }),
        ('Organization', {
            'fields': ('region', 'tessera_number', 'status')
        }),
        ('Contact', {
            'fields': ('phone', 'bio')
        }),
        ('Dates', {
            'fields': ('date_joined', 'last_updated'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'amount', 'status', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('donor_name', 'donor_email', 'transaction_id')
    readonly_fields = ('transaction_id', 'created_at', 'completed_at')
    fieldsets = (
        ('Donor Info', {
            'fields': ('donor_name', 'donor_email', 'donor_phone', 'is_anonymous', 'member')
        }),
        ('Donation Details', {
            'fields': ('amount', 'currency', 'message')
        }),
        ('Payment', {
            'fields': ('status', 'payment_method', 'transaction_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_type', 'is_published', 'order')
    list_filter = ('page_type', 'is_published')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Page Info', {
            'fields': ('title', 'slug', 'page_type')
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('full-width',)
        }),
        ('Organization', {
            'fields': ('order', 'is_published')
        }),
    )
