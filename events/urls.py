from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<eid>[0-9]+)$', views.event, name='event'),
    url(r'^$', views.index, name='index'),
    url(r'^extern/(?P<uuid>[0-9a-z\-]+)?$', views.event_extern, name='extern'),
    url(r'^admin/$', views.admin_index, name='admin_index'),
    url(r'^admin/list/$', views.admin_list_events, name='admin_list_events'),
    url(r'^admin/add/$', views.admin_add, name='admin_add'),
    url(r'^admin/edit/(?P<eid>[0-9]+)$', views.admin_edit, name='admin_edit'),
    url(r'^admin/export/(?P<eid>[0-9]+)$', views.admin_export_csv, name='admin_export_csv'),
    url(r'^admin/view/(?P<eid>[0-9]+)/registrations$', views.admin_list_registrations, name='admin_list_registrations'),
    url(r'^admin/management/(?P<eid>[0-9]+)$', views.admin_management, name='admin_management'),
    url(r'^admin/management/list_registrations/(?P<eid>[0-9]+)$', views.management_list_users, name='admin_management_list'),
    url(r'^admin/management/(?P<eid>[0-9]+)/info/(?P<type>[a-zA-Z_]+)/(?P<iid>[0-9]+)$', views.management_info_user, name='admin_management_list'),
    url(r'^admin/management/(?P<eid>[0-9]+)/ack/(?P<type>[a-zA-Z_]+)/(?P<iid>[0-9]+)$', views.management_ack, name='admin_management_ack'),
    url(r'^admin/management/(?P<eid>[0-9]+)/del/(?P<type>[a-zA-Z_]+)/(?P<iid>[0-9]+)$', views.management_nl_del, name='admin_management_del'),
    url(r'^admin/management/(?P<eid>[0-9]+)/nl_info/(?P<type>[a-zA-Z_]+)/(?P<iid>[0-9]+)$', views.management_nl_info_user, name='admin_management_list'),
    url(r'^admin/management/nl_ack$', views.management_nl_ack, name='admin_management_nl_ack'),
    url(r'^admin/management/(?P<eid>[0-9]+)/nl_ack_popup/(?P<iid>[0-9]+)$', views.management_nl_ack_popup, name='admin_management_nl_ack_popup'),
]

