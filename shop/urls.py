
from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sells$', views.sells, name='sells'),
    url(r'^pack$', views.pack, name='pack'),
    url(r'^history$', views.history, name='history'),
    url(r'^admin$', views.admin, name='admin'),
    url(r'^admin/product/delete/(?P<pid>[0-9]+)', views.product_delete, name='product_delete'),
    url(r'^admin/product/add$', views.product_add, name='product_add'),
    url(r'^admin/pack/delete/(?P<pid>[0-9]+)', views.pack_delete, name='pack_delete'),
    url(r'^admin/pack/add$', views.pack_add, name='pack_add'),
]

