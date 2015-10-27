from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^browse/(?P<path>.*)$', views.browse, name='browse'),
    url(r'^permissions/(?P<path>.*)$', views.permissions, name='permissions'),
    url(r'^delete/(?P<model>[0-9A-Za-z]+)/(?P<pid>[0-9]+)$', views.permissions_delete, name='permissions_delete'),
]

