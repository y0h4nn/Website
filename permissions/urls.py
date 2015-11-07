
from django.conf.urls import url
from . import views

urlpatterns = [
    url('^users$', views.users, name='users'),
    url('^groups$', views.groups, name='groups'),
    url('^(?P<gid>[0-9]+)/members', views.custom_member_list, name='custom_member_list'),
]

