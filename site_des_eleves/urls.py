"""site_des_eleves URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('news.urls', namespace="news")),
    url(r'^settings$', include('core.urls', namespace="core")),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^poll/', include('poll.urls', namespace='poll')),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^webmail/', include('webmail.urls', namespace='webmail')),
    url(r'^bde/', include('bde.urls', namespace='bde')),
    url(r'^covoit/', include('carshare.urls', namespace='carshare')),
    url(r'^notifications/', include('notifications.urls', namespace='notifications')),
]
