"""
Admin configuration for the shortener app.
"""

from django.contrib import admin
from .models import URL, ClickEvent


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    """Admin interface for URL model."""
    
    list_display = [
        'short_code',
        'original_url',
        'click_count',
        'custom_code',
        'created_at',
        'expiry_date',
        'is_active'
    ]
    
    list_filter = [
        'custom_code',
        'created_at',
        'expiry_date'
    ]
    
    search_fields = [
        'short_code',
        'original_url'
    ]
    
    readonly_fields = [
        'short_code',
        'created_at',
        'click_count'
    ]
    
    ordering = ['-created_at']
    
    def is_active(self, obj):
        """Display whether URL is active or expired."""
        return obj.is_active
    
    is_active.boolean = True
    is_active.short_description = 'Active'


@admin.register(ClickEvent)
class ClickEventAdmin(admin.ModelAdmin):
    """Admin interface for ClickEvent model."""
    
    list_display = [
        'url',
        'timestamp',
        'ip_address',
        'user_agent_short'
    ]
    
    list_filter = [
        'timestamp',
    ]
    
    search_fields = [
        'url__short_code',
        'ip_address'
    ]
    
    readonly_fields = [
        'url',
        'timestamp',
        'ip_address',
        'user_agent'
    ]
    
    ordering = ['-timestamp']
    
    def user_agent_short(self, obj):
        """Display truncated user agent."""
        return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
    
    user_agent_short.short_description = 'User Agent'
