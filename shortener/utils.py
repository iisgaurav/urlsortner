import string
import random
from django.core.cache import cache
from .models import URL


BASE62_CHARS = string.digits + string.ascii_lowercase + string.ascii_uppercase


def encode_base62(num):
    if num == 0:
        return BASE62_CHARS[0]
    
    encoded = ''
    while num > 0:
        encoded = BASE62_CHARS[num % 62] + encoded
        num //= 62
    
    return encoded


def generate_short_code(url_id):
    return encode_base62(url_id)


def generate_random_code(length=6):
    return ''.join(random.choices(BASE62_CHARS, k=length))


def is_valid_custom_code(code):
    if not code:
        return False, "Code cannot be empty"
    
    if len(code) < 3 or len(code) > 10:
        return False, "Code must be between 3 and 10 characters"
    
    if not code.isalnum():
        return False, "Code must contain only alphanumeric characters"
    
    if URL.objects.filter(short_code=code).exists():
        return False, "Code is already taken"
    
    return True, None


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_url_from_cache(short_code):
    cache_key = f"url:{short_code}"
    return cache.get(cache_key)


def set_url_in_cache(short_code, url_data, timeout=3600):
    cache_key = f"url:{short_code}"
    cache.set(cache_key, url_data, timeout=timeout)


def invalidate_url_cache(short_code):
    cache_key = f"url:{short_code}"
    cache.delete(cache_key)
