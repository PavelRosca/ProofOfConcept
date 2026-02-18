from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


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
