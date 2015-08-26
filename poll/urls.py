from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<pid>[0-9]+)$', views.question, name='poll'),
    url(r'^/?$', views.poll_index, name='index'),
    url(r'^thanks', views.thanks, name='thanks'),
    url(r'^already', views.already, name='already'),
    url(r'^admin/add/$', views.admin_add_poll, name='admin_add_poll'),
    url(r'^admin/delete/$', views.admin_delete, name='admin_delete'),
    url(r'^admin/view/(?P<pid>[0-9]+)$', views.admin_question, name='admin_question'),
    url(r'^admin/edit/(?P<pid>[0-9]+)$', views.admin_question, name='admin_edit_poll'),
    url(r'^admin/list/$', views.admin_list, name="admin_list"),
    url(r'^admin/$', views.admin_index, name='admin'),
]

