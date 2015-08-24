from django.conf.urls import include, url
from . import views


PREFIX = "core:"

urlpatterns = [
    url(r'^$', views.settings, name='settings'),
]
