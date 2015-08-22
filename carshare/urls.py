
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^(?P<aid>[0-9]+)$', views.show, name='show'),
    url(r'^(?P<aid>[0-9]+)/(?P<rid>[0-9]+)/(?P<state>[a-z]+)$', views.action, name='action'),
]

