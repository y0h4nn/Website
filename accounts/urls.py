from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^(?P<username>[a-zA-Z0-9]+)$', views.show, name='show'),
    url(r'^(?P<username>[a-zA-Z0-9]+)/edit$', views.edit, name='edit'),
]
