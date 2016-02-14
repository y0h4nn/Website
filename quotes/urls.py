from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^add_quote$', views.add_quote, name='add_quote'),
    url(r'^manage_prof$', views.manage_prof, name='manage_prof'),
    url(r'^manage_quotes$', views.manage_quotes, name='manage_quotes'),
    url(r'^del_quote/(?P<qid>[0-9]+)$', views.del_quote, name='del_quote'),
    url(r'^del_prof/(?P<pid>[0-9]+)$', views.del_prof, name='del_prof'),
    url(r'^approve_quote/(?P<qid>[0-9]+)$', views.approve_quote, name='approve_quote'),
]

