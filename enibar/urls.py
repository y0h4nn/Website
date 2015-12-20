from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^note$', views.request_note, name="request_note"),
    url(r'^history$', views.request_history, name="request_history"),
    url(r'^show_history$', views.show_history, name="show_history"),
]

