from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^edit/(?P<nid>[0-9]+)$', views.edit, name='edit'),
    url(r'^delete/(?P<nid>[0-9]+)$', views.delete, name='delete')
]

