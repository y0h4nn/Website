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
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^', include('news.urls', namespace="news")),
    url(r'^settings/', include('core.urls', namespace="core")),
    url(r'^accounts/', include('accounts.urls', namespace="accounts")),
    url(r'^accounts/password_reset/$', auth_views.password_reset, {'template_name': 'accounts/password_reset.html'}, name='password_reset'),
    url(r'^accounts/password_reset/done/$', auth_views.password_reset_done, {'template_name': 'accounts/password_reset_done.html'}, name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/a$', auth_views.password_reset_confirm, {'template_name': 'accounts/password_reset_confirm.html'}, name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', auth_views.password_reset_complete, {'template_name': 'accounts/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^poll/', include('poll.urls', namespace='poll')),
    url(r'^events/', include('events.urls', namespace='events')),
    url(r'^webmail/', include('webmail.urls', namespace='webmail')),
    url(r'^bde/', include('bde.urls', namespace='bde')),
    url(r'^covoit/', include('carshare.urls', namespace='carshare')),
    url(r'^notifications/', include('notifications.urls', namespace='notifications')),
    url(r'^shop/', include('shop.urls', namespace='shop')),
    url(r'^pizzas/', include('pizza.urls', namespace='pizza')),
    url(r'^help/', include('help.urls', namespace='help')),
]
