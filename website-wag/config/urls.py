"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls
from .views import api_status, cms_page, legacy_html_page_redirect

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.svg', permanent=False)),
    path('api-status/', api_status, name='api-status'),
    path('admin/', admin.site.urls),
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/<slug:slug>/', cms_page, name='cms-page'),
    path('<slug:page>.html', legacy_html_page_redirect, name='legacy-html-page'),
    path('api/', include('core.urls')),
    path('api/auth/', include('rest_framework.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include(wagtail_urls)),
]

# Media files (development only)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

