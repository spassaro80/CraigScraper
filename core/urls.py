from django.urls import path
from .views import index,bones_scraper

urlpatterns = [
    path('', index, name='index'),
    path('bonesscraper', bones_scraper, name='bones_scraper')
]