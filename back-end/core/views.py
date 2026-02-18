from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sector, Region, Project, Member, Donation, StaticPage
from .serializers import (
    SectorSerializer, RegionSerializer, ProjectSerializer,
    MemberSerializer, DonationSerializer, StaticPageSerializer
)


class SectorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Sectors
    - List all sectors
    - Get sector details with regions
    """
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['region_type']
    ordering_fields = ['order', 'created_at']
    
    @action(detail=True, methods=['get'])
    def regions(self, request, pk=None):
        """Get all regions for a specific sector"""
        sector = self.get_object()
        regions = sector.regions.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Regions
    - List all regions
    - Get region details with members
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sector', 'active']
    search_fields = ['name', 'code']
    
    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members in a specific region"""
        region = self.get_object()
        members = region.members.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Projects
    - List all projects
    - Get project details
    - Filter by status or sector
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_featured']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'start_date', 'budget']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get only featured projects"""
        featured = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get active/in-progress projects"""
        active = self.queryset.filter(status='in_corso')
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)


class MemberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Members
    - List all members
    - Get member details
    """
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'region']
    search_fields = ['user__first_name', 'user__last_name', 'tessera_number']


class DonationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Donations
    - List donations
    - Create donation
    - Filter by status
    """
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method']
    ordering_fields = ['created_at', 'amount']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get donation statistics"""
        total_donations = Donation.objects.filter(status='completed').count()
        total_amount = Donation.objects.filter(status='completed').values_list('amount', flat=True)
        total_value = sum(total_amount) if total_amount else 0
        
        return Response({
            'total_donations': total_donations,
            'total_value': float(total_value),
            'currency': 'EUR'
        })


class StaticPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for Static Pages
    - List all pages
    - Get page by slug
    """
    queryset = StaticPage.objects.filter(is_published=True)
    serializer_class = StaticPageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['page_type']
    search_fields = ['title', 'slug']
    lookup_field = 'slug'
