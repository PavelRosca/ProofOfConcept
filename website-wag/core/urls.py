from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SectorViewSet, RegionViewSet, ProjectViewSet,
    MemberViewSet, DonationViewSet, StaticPageViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'sectors', SectorViewSet, basename='sector')
router.register(r'regions', RegionViewSet, basename='region')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'members', MemberViewSet, basename='member')
router.register(r'donations', DonationViewSet, basename='donation')
router.register(r'pages', StaticPageViewSet, basename='staticpage')

app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
]
