from django.conf.urls import url
from .views import *

app_name = 'base'
urlpatterns = [
    url(r'^$', index, name='index'),
    # categories
    url(r'^categories/', category_list, name='category_list'),
    url(r'^category/create/$', category_create, name='category_create'),
    url(r'^category/update/(?P<category_id>\d+)/$', category_update, name='category_update'),
    url(r'^category/delete/(?P<category_id>\d+)/$', category_delete, name='category_delete'),

    # books 
    url(r'^category/(?P<category_id>\d+)/books/$', book_list, name='book_list'),
    url(r'^book/create/$', book_create, name='book_create'),
    url(r'^book/(?P<book_id>\d+)/$', book_detail, name='book_detail'),
    url(r'^book/update/(?P<book_id>\d+)/$', book_update, name='book_update'),
    url(r'^book/delete/(?P<book_id>\d+)/$', book_delete, name='book_delete'),
]
