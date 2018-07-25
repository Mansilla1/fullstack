from django.conf.urls import url
from .views import scraping_create

app_name = 'scraper'
urlpatterns = [
    url(r'^/', scraping_create, name='scraping_create'),
]