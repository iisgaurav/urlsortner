"""
App configuration for shortener.
"""

from django.apps import AppConfig


class ShortenerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shortener'
    verbose_name = 'URL Shortener'
    
    def ready(self):
        """
        Import tasks module when app is ready.
        This ensures Celery can discover tasks.
        """
        import shortener.tasks  # noqa
