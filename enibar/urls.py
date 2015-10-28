from django.conf.urls import include, url
from . import views

from rest_framework import routers, serializers, viewsets
router = routers.DefaultRouter()
router.register('notes', views.NoteViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]

