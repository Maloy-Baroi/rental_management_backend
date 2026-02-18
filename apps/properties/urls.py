from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, PropertyViewSet, UnitViewSet, UtilityTypeViewSet

router = DefaultRouter()
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'properties', PropertyViewSet, basename='property')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'utility-types', UtilityTypeViewSet, basename='utility-type')

urlpatterns = [
    path('', include(router.urls)),
]

