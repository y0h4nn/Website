from django.conf.urls import include, url
from rest_framework import routers
from .views.events import EventViewSet


router = routers.DefaultRouter()
router.register('events', EventViewSet)

urlpatterns = [
    url('^', include(router.urls)),
]

