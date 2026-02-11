"""
Celery tasks for asynchronous processing.
"""

from celery import shared_task
from django.utils import timezone
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def log_click_event(self, url_id, ip_address, user_agent):
    from .models import URL, ClickEvent
    
    try:
        url_obj = URL.objects.get(id=url_id)
        
        # Create click event record
        ClickEvent.objects.create(
            url=url_obj,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        # Increment click count
        url_obj.click_count += 1
        url_obj.save(update_fields=['click_count'])
        
        logger.info(f"Logged click for {url_obj.short_code} (total: {url_obj.click_count})")
        
        return {
            'success': True,
            'url_id': url_id,
            'click_count': url_obj.click_count
        }
        
    except URL.DoesNotExist:
        logger.error(f"URL with id {url_id} not found")
        return {'success': False, 'error': 'URL not found'}
    
    except Exception as exc:
        logger.error(f"Error logging click event: {exc}")
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=2 ** self.request.retries)


@shared_task
def cleanup_expired_urls():
    from .models import URL
    from .utils import invalidate_url_cache
    
    try:
        expired_urls = URL.objects.filter(
            expiry_date__isnull=False,
            expiry_date__lt=timezone.now()
        )
        
        count = expired_urls.count()
        
        for url in expired_urls:
            invalidate_url_cache(url.short_code)
            logger.info(f"Cleaning up expired URL: {url.short_code}")
        
        expired_urls.delete()
        
        logger.info(f"Cleanup completed: Removed {count} expired URLs")
        
        return {
            'success': True,
            'deleted_count': count,
            'timestamp': timezone.now().isoformat()
        }
        
    except Exception as exc:
        logger.error(f"Error during cleanup: {exc}")
        return {
            'success': False,
            'error': str(exc)
        }


@shared_task
def update_cache_for_url(short_code):
    from .models import URL
    from .utils import set_url_in_cache
    
    try:
        url_obj = URL.objects.get(short_code=short_code)
        
        # Update cache with fresh data
        url_data = {
            'original_url': url_obj.original_url,
            'expiry_date': url_obj.expiry_date.isoformat() if url_obj.expiry_date else None,
        }
        
        set_url_in_cache(short_code, url_data)
        
        logger.info(f"Cache refreshed for {short_code}")
        
        return {'success': True, 'short_code': short_code}
        
    except URL.DoesNotExist:
        logger.error(f"URL {short_code} not found for cache update")
        return {'success': False, 'error': 'URL not found'}
