from rest_framework import serializers
from .models import Sector, Region, Project, Member, Donation, StaticPage
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class SectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = ('id', 'name', 'region_type', 'description', 'order', 'created_at')


class RegionSerializer(serializers.ModelSerializer):
    sector_name = serializers.CharField(source='sector.name', read_only=True)
    
    class Meta:
        model = Region
        fields = ('id', 'name', 'code', 'sector', 'sector_name', 'description', 'contact_email', 'contact_phone', 'active')


class ProjectSerializer(serializers.ModelSerializer):
    sectors_data = SectorSerializer(source='sectors', many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = ('id', 'title', 'slug', 'description', 'short_description', 'status', 'sectors', 'sectors_data', 'budget', 'start_date', 'end_date', 'image', 'is_featured', 'order', 'created_at')


class MemberSerializer(serializers.ModelSerializer):
    user_data = UserSerializer(source='user', read_only=True)
    region_name = serializers.CharField(source='region.name', read_only=True)
    
    class Meta:
        model = Member
        fields = ('id', 'user', 'user_data', 'region', 'region_name', 'tessera_number', 'status', 'phone', 'bio', 'date_joined')


class DonationSerializer(serializers.ModelSerializer):
    donor_member_name = serializers.CharField(source='member.user.get_full_name', read_only=True)
    
    class Meta:
        model = Donation
        fields = ('id', 'donor_name', 'donor_email', 'donor_phone', 'member', 'donor_member_name', 'amount', 'currency', 'status', 'payment_method', 'message', 'is_anonymous', 'created_at')
        read_only_fields = ('created_at',)


class StaticPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaticPage
        fields = ('id', 'slug', 'title', 'page_type', 'content', 'is_published', 'created_at', 'updated_at')
