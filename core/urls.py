from django.conf.urls import include, url
from . import views
from . import register


PREFIX = "core:"

urlpatterns = [
    url(r'^$', views.index, name='index'),
]

register.menu_item('Accueil', PREFIX + 'index')
