from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# TODO: Register viewsets here when they are implemented
# Example: router.register(r'contracts', RentalContractViewSet, basename='contract')

urlpatterns = [
    path('', include(router.urls)),
]

