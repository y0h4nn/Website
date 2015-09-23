from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.create, name='create'),
    url(r'^edit/(?P<nid>[0-9]+)$', views.edit, name='edit'),
    url(r'^delete/(?P<nid>[0-9]+)$', views.delete, name='delete'),
    url(r'^comments/(?P<nid>[0-9]+)$', views.comment, name='comment'),
    url(r'^del_comment/(?P<cid>[0-9]+)$', views.del_comment, name='del_comment'),
]

