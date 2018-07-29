from django.conf.urls import url, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'books', BookViewSet)


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

    # rest api
    url(r'^rest-data/', include(router.urls)),
    # category rest
    url(r'^rest-categories/$', rest_category_list),
    url(r'^rest-categories/(?P<pk>[0-9]+)/$', rest_category_detail),
    # book rest
    url(r'^rest-books/$', rest_book_list),
    url(r'^rest-books/(?P<pk>[0-9]+)/$', rest_book_detail),
]
