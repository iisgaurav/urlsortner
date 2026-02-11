"""
Database models for URL shortener application.
"""

from django.db import models
from django.utils import timezone


class URL(models.Model):
    
    original_url = models.URLField(
        max_length=2048,
        help_text="The original long URL to be shortened"
    )
    
    short_code = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        help_text="Unique short code identifier"
    )
    
    custom_code = models.BooleanField(
        default=False,
        help_text="True if custom alias, False if auto-generated"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when URL was created"
    )
    
    expiry_date = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Optional expiration date for the URL"
    )
    
    click_count = models.IntegerField(
        default=0,
        help_text="Total number of clicks (cached, updated by Celery)"
    )
    
    class Meta:
        db_table = 'urls'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['short_code']),
            models.Index(fields=['expiry_date']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.short_code} -> {self.original_url[:50]}"
    
    def is_expired(self):
        """Check if the URL has expired."""
        if self.expiry_date is None:
            return False
        return timezone.now() > self.expiry_date
    
    @property
    def is_active(self):
        """Check if URL is currently active (not expired)."""
        return not self.is_expired()


class ClickEvent(models.Model):
    
    url = models.ForeignKey(
        URL,
        on_delete=models.CASCADE,
        related_name='clicks',
        help_text="The URL that was clicked"
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="When the click occurred"
    )
    
    ip_address = models.GenericIPAddressField(
        help_text="IP address of the requester"
    )
    
    user_agent = models.TextField(
        help_text="User agent string from the request"
    )
    
    class Meta:
        db_table = 'click_events'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['url', '-timestamp']),
            models.Index(fields=['-timestamp']),
        ]
    
    def __str__(self):
        return f"Click on {self.url.short_code} at {self.timestamp}"
