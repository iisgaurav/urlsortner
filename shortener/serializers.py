"""
Serializers for the URL shortener API.
"""

from rest_framework import serializers
from django.conf import settings
from .models import URL, ClickEvent
from .utils import is_valid_custom_code


class URLCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new shortened URLs.
    """
    
    custom_code = serializers.CharField(
        max_length=10,
        required=False,
        allow_blank=True,
        help_text="Optional custom short code (3-10 alphanumeric characters)"
    )
    
    short_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = URL
        fields = ['original_url', 'custom_code', 'expiry_date', 'short_url', 'created_at']
        read_only_fields = ['short_url', 'created_at']
    
    def validate_custom_code(self, value):
        """Validate custom code if provided."""
        if value:
            is_valid, error_message = is_valid_custom_code(value)
            if not is_valid:
                raise serializers.ValidationError(error_message)
        return value
    
    def validate_original_url(self, value):
        """Validate the original URL format."""
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError(
                "URL must start with http:// or https://"
            )
        return value
    
    def get_short_url(self, obj):
        """Generate the full short URL."""
        domain = settings.SHORT_URL_DOMAIN.rstrip('/')
        return f"{domain}/{obj.short_code}"


class URLAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for URL analytics and statistics.
    """
    
    total_clicks = serializers.IntegerField(source='click_count', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    recent_clicks = serializers.SerializerMethodField()
    
    class Meta:
        model = URL
        fields = [
            'short_code',
            'original_url',
            'total_clicks',
            'created_at',
            'expiry_date',
            'is_active',
            'custom_code',
            'recent_clicks'
        ]
    
    def get_recent_clicks(self, obj):
        """Get the 10 most recent click events."""
        recent = obj.clicks.all()[:10]
        return ClickEventSerializer(recent, many=True).data


class ClickEventSerializer(serializers.ModelSerializer):
    """
    Serializer for individual click events.
    """
    
    class Meta:
        model = ClickEvent
        fields = ['timestamp', 'ip_address', 'user_agent']
