from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^note$', views.request_note, name="request_note"),
    url(r'^category$', views.request_category, name="request_category"),
    url(r'^price_description$', views.request_price_description, name="request_price_description"),
    url(r'^product$', views.request_product, name="request_product"),
    url(r'^price$', views.request_price, name="request_price"),
    url(r'^history$', views.request_history, name="request_history"),
]

