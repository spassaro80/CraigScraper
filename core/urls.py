from django.urls import path
from .views import HomePageView,SamplePageView,index,scraper

urlpatterns = [
    path('', index, name='index'),
    path('sample/', SamplePageView.as_view(), name='sample'),
    path('results/', scraper, name='scraper'),
]