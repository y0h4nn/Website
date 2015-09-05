from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<eid>[0-9]+)$', views.event, name='event'),
    url(r'^/?$', views.index, name='index'),
    url(r'^admin/$', views.admin_index, name='admin_index'),
    url(r'^admin/list/$', views.admin_list_events, name='admin_list_events'),
    url(r'^admin/add/$', views.admin_add, name='admin_add'),
    url(r'^admin/view/(?P<eid>[0-9]+)$', views.admin_view, name='admin_view'),
    url(r'^admin/edit/(?P<eid>[0-9]+)$', views.admin_edit, name='admin_edit'),
    url(r'^admin/export/(?P<eid>[0-9]+)$', views.admin_export_csv, name='admin_export_csv'),
    url(r'^admin/view/(?P<eid>[0-9]+)/registrations$', views.admin_list_registrations, name='admin_list_registrations'),
]

