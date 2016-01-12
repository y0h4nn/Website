from django.conf.urls import include, url
from rest_framework import routers
from .views.events import EventViewSet
from .views.users import UserViewSet


router = routers.DefaultRouter()
router.register('events', EventViewSet)
router.register('users', UserViewSet)


urlpatterns = [
    url('^', include(router.urls)),
]

