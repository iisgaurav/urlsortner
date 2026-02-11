"""
Rate limiting middleware using Redis.
"""

from django.http import JsonResponse
from django.core.cache import cache
from django.conf import settings
import time
import logging

logger = logging.getLogger(__name__)


class RateLimitMiddleware:
    """
    Redis-based rate limiting middleware.
    
    Limits requests per IP address using a sliding window algorithm.
    Configuration:
    - RATE_LIMIT_REQUESTS: Number of allowed requests
    - RATE_LIMIT_WINDOW: Time window in seconds
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.rate_limit_requests = getattr(settings, 'RATE_LIMIT_REQUESTS', 10)
        self.rate_limit_window = getattr(settings, 'RATE_LIMIT_WINDOW', 60)
    
    def __call__(self, request):
        if self.should_rate_limit(request):
            if not self.check_rate_limit(request):
                logger.warning(f"Rate limit exceeded for IP: {self.get_client_ip(request)}")
                return JsonResponse(
                    {
                        'error': 'Rate limit exceeded',
                        'message': f'Maximum {self.rate_limit_requests} requests per {self.rate_limit_window} seconds allowed',
                    },
                    status=429
                )
        
        response = self.get_response(request)
        return response
    
    def should_rate_limit(self, request):
        """
        Determine if the request should be rate limited.
        Only apply to URL creation endpoint.
        """
        if request.path == '/api/shorten/' and request.method == 'POST':
            return True
        return False
    
    def check_rate_limit(self, request):
        """
        Check if request is within rate limit.
        
        Uses Redis to track request count per IP in a sliding window.
        
        Returns:
            True if request is allowed, False if rate limit exceeded
        """
        ip_address = self.get_client_ip(request)
        current_time = int(time.time())
        
        cache_key = f"ratelimit:{ip_address}:shorten"
        
        request_timestamps = cache.get(cache_key, [])
        
        window_start = current_time - self.rate_limit_window
        request_timestamps = [ts for ts in request_timestamps if ts > window_start]
        
        if len(request_timestamps) >= self.rate_limit_requests:
            return False
        
        request_timestamps.append(current_time)
        
        cache.set(cache_key, request_timestamps, timeout=self.rate_limit_window)
        
        return True
    
    def get_client_ip(self, request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
