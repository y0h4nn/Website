from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^browse/(?P<path>.*)$', views.browse, name='browse'),
    url(r'^permissions/(?P<path>.*)$', views.permissions, name='permissions'),
    url(r'^album/add$', views.add_album, name='add_album'),
]

