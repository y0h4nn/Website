from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<eid>[0-9]+)$', views.event, name='event'),
]

