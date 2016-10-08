from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^note$', views.request_note, name="request_note"),
    url(r'^photos$', views.get_photo_paths, name="photo_paths"),
    url(r'^history$', views.request_history, name="request_history"),
    url(r'^show_history/(?P<page>[0-9]+)?$', views.show_history, name="show_history"),
]

