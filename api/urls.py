from django.conf.urls import include, url
from rest_framework import routers
from .views.events import EventViewSet, FormulaViewSet
from .views.users import UserViewSet


router = routers.DefaultRouter()
router.register('events', EventViewSet)
router.register('users', UserViewSet)
router.register('formulas', FormulaViewSet)


urlpatterns = [
    url('^', include(router.urls)),
]

