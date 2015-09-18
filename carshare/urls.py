
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^edit/(?P<aid>[0-9]+)$', views.edit, name='edit'),
    url(r'^delete/announce/(?P<aid>[0-9]+)$', views.delete, name='delete'),
    url(r'^delete/registration/(?P<rid>[0-9]+)$', views.delete_registration, name='delete_registration'),
    url(r'^(?P<aid>[0-9]+)$', views.show, name='show'),
    url(r'^(?P<aid>[0-9]+)/(?P<rid>[0-9]+)/(?P<state>[a-z]+)$', views.action, name='action'),
]

