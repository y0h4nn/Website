from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin$', views.admin_manage_partnerships, name='admin_index'),
    url(r'^edit/(?P<nid>[0-9]+)$', views.admin_edit, name='admin_edit'),
    url(r'^delete/(?P<nid>[0-9]+)$', views.admin_delete, name='admin_delete'),
    url(r'^admin_add_partnership$', views.admin_add_partnership, name='admin_add_partnership'),
]
