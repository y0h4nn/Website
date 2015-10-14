from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^browse/(?P<path>.*)$', views.browse, name='browse'),
    url(r'^album/add$', views.add_album, name='add_album'),
]

