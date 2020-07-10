from django.urls import path
from .views import index,scraper,bones_scraper

urlpatterns = [
    path('', index, name='index'),
    path('results/', scraper, name='scraper'),
    path('bonesscraper', bones_scraper, name='bones_scraper')
]