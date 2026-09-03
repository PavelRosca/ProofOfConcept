from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('key', 'label_it', 'order', 'is_active', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('key',)
    ordering = ('order',)
