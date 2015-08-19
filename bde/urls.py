from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^contributors$', views.contributors, name='contributors'),
    url(r'^contributors/(?P<id>[0-9]+)$', views.detail, name='detail'),
]

