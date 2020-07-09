from django.urls import path
from .views import index,scraper

urlpatterns = [
    path('', index, name='index'),
    path('results/', scraper, name='scraper'),
]