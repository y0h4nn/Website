from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<pid>[0-9]+)$', views.question, name='poll'),
    url(r'^thanks', views.thanks, name='thanks'),
    url(r'^already', views.already, name='already'),
    url(r'^admin/view/(?P<pid>[0-9]+)$', views.admin_view_poll, name='admin_view_poll'),
    url(r'^admin/add$', views.admin_add_poll, name='admin_add_poll'),
    url(r'^admin', views.admin_index, name='admin'),
]
