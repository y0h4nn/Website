from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^read/(?P<nid>[0-9]+)$', views.read, name='read'),
]

