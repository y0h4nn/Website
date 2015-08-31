
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sell$', views.sell, name='sell'),
    url(r'^history$', views.history, name='history'),
    url(r'^admin$', views.admin, name='admin'),
    url(r'^admin/delete/(?P<pid>[0-9]+)', views.delete, name='delete')
]

