from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RentalContractViewSet, RentalContractParticipantViewSet

router = DefaultRouter()
router.register(r'contracts', RentalContractViewSet, basename='contract')
router.register(r'participants', RentalContractParticipantViewSet, basename='participant')

urlpatterns = [
    path('', include(router.urls)),
]

