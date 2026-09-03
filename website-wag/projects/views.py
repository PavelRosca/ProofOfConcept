from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods

from members.access import active_member_required

from .models import Category


@require_http_methods(['GET'])
@active_member_required
def category_detail(request, key):
    category = get_object_or_404(Category, key=key, is_active=True)
    return render(request, 'site/category_detail.html', {'category': category})
