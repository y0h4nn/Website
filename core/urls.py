from django.conf.urls import include, url
from . import views


PREFIX = "core:"

urlpatterns = [
    url('^$', views.settings, name='settings'),
    url('^api$', views.api, name='api'),
]
