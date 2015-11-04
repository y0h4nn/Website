from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^request$', views.account_request, name='request'),
    url(r'^list-request$', views.list_request, name='list_request'),
    url(r'^list-request/error/(?P<error>[a-z]+)$', views.list_request, name='list_request'),
    url(r'^confirmation-request$', views.confirmation_request, name='confirmation'),
    url(r'^accept-request/(?P<rid>[0-9]+)', views.accept_request, name='accept-request'),
    url(r'^reject-request/(?P<rid>[0-9]+)', views.reject_request, name='reject-request'),
    url(r'^(?P<username>[_a-zA-Z0-9éèÃ©®§«´‰¯¨¢œ\\\'@,. -]+)$', views.show, name='show'),
    url(r'^(?P<username>[_a-zA-Z0-9éèÃ©®§«´‰¯¨¢œ\\\'@,. -]+)/edit$', views.edit, name='edit'),
    url(r'^members/$', views.members, name='members'),
    url(r'^groups/$', views.groups, name='groups'),
]

