from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<aid>[0-9]+)$', views.details, name='details'),
    url(r'^members/(?P<aid>[0-9]+)$', views.asso_members, name='members'),
    url(r'^manage_members/(?P<aid>[0-9]+)$', views.asso_manage_members, name='manage_members'),
    url(r'^edit/(?P<aid>[0-9]+)$', views.asso_edit, name='edit'),
    url(r'^management$', views.asso_managment, name='managment'),
    url(r'^management/settings/(?P<aid>[0-9]+)$', views.asso_settings, name='settings'),
    url(r'^management/delete/(?P<aid>[0-9]+)$', views.asso_delete, name='delete'),
    url(r'^management/create', views.asso_create, name='create'),
]

