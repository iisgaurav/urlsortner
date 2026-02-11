from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
import logging

from .models import URL
from .serializers import URLCreateSerializer, URLAnalyticsSerializer
from .utils import generate_short_code, get_client_ip
from .tasks import log_click_event

logger = logging.getLogger(__name__)


@api_view(['POST'])
def create_short_url(request):
    serializer = URLCreateSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(
            {'error': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    custom_code = serializer.validated_data.get('custom_code')
    
    if custom_code:
        url_obj = serializer.save(
            short_code=custom_code,
            custom_code=True
        )
    else:
        url_obj = serializer.save(short_code='temp')
        url_obj.short_code = generate_short_code(url_obj.id)
        url_obj.save(update_fields=['short_code'])
    
    cache_key = f"url:{url_obj.short_code}"
    cache_data = {
        'id': url_obj.id,
        'original_url': url_obj.original_url,
        'expiry_date': url_obj.expiry_date.isoformat() if url_obj.expiry_date else None,
    }
    
    # Cache the URL for 1 hour
    cache.set(cache_key, cache_data, timeout=3600)
    
    logger.info(f"Created short URL: {url_obj.short_code} -> {url_obj.original_url}")
    
    # Return response
    response_serializer = URLCreateSerializer(url_obj)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def redirect_to_url(request, short_code):
    cache_key = f"url:{short_code}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        logger.debug(f"Cache HIT for {short_code}")
        url_id = cached_data['id']
        original_url = cached_data['original_url']
        expiry_date = cached_data.get('expiry_date')
        
        if expiry_date:
            expiry_dt = timezone.datetime.fromisoformat(expiry_date)
            if timezone.now() > expiry_dt:
                return Response(
                    {'error': 'This link has expired'},
                    status=status.HTTP_410_GONE
                )
    else:
        logger.debug(f"Cache MISS for {short_code}")
        
        try:
            url_obj = URL.objects.get(short_code=short_code)
        except URL.DoesNotExist:
            return Response(
                {'error': 'Short URL not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if url_obj.is_expired():
            return Response(
                {'error': 'This link has expired'},
                status=status.HTTP_410_GONE
            )
        
        url_id = url_obj.id
        original_url = url_obj.original_url
        
        cache_data = {
            'id': url_obj.id,
            'original_url': url_obj.original_url,
            'expiry_date': url_obj.expiry_date.isoformat() if url_obj.expiry_date else None,
        }
        cache.set(cache_key, cache_data, timeout=3600)
        logger.info(f"Cached URL: {short_code}")
    
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
    
    log_click_event.delay(url_id, ip_address, user_agent)
    
    return redirect(original_url)


@api_view(['GET'])
def get_analytics(request, short_code):
    url_obj = get_object_or_404(URL, short_code=short_code)
    serializer = URLAnalyticsSerializer(url_obj)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_short_url(request, short_code):
    url_obj = get_object_or_404(URL, short_code=short_code)
    
    cache_key = f"url:{short_code}"
    cache.delete(cache_key)
    
    url_obj.delete()
    
    logger.info(f"Deleted short URL: {short_code}")
    
    return Response(
        {'message': 'URL deleted successfully'},
        status=status.HTTP_200_OK
    )
