"""
URL routing for the shortener app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('api/shorten/', views.create_short_url, name='create_short_url'),
    path('api/analytics/<str:short_code>/', views.get_analytics, name='get_analytics'),
    path('api/urls/<str:short_code>/', views.delete_short_url, name='delete_short_url'),
    
    path('<str:short_code>/', views.redirect_to_url, name='redirect_to_url'),
]
