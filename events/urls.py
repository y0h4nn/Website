from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<eid>[0-9]+)$', views.event, name='event'),
    url(r'^admin/$', views.admin_index, name='admin_index'),
    url(r'^admin/add/$', views.admin_add, name='admin_add'),
]

