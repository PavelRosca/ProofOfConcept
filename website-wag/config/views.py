from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from core.models import StaticPage


@require_http_methods(["GET"])
def cms_page(request, slug):
    """Render admin-managed CMS page content from StaticPage."""
    page_obj = get_object_or_404(StaticPage, slug=slug, is_published=True)
    return render(request, 'cms/page.html', {'page_obj': page_obj})


@require_http_methods(["GET"])
def legacy_html_page_redirect(request, page):
    if page == 'index':
        return redirect('/', permanent=True)
    return redirect(f'/{page}/', permanent=True)


@require_http_methods(["GET"])
def api_status(request):
    """API status check - root endpoint"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Partito Politico Backend API',
        'version': '1.0',
        'endpoints': {
            'admin': '/admin/',
            'api_auth': '/api/auth/',
            'accounts': '/accounts/',
        }
    })
