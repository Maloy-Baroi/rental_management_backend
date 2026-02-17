from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView,
    UserProfileView,
    PasswordChangeView,
    HouseholdViewSet
)

router = DefaultRouter()
router.register(r'households', HouseholdViewSet, basename='household')

urlpatterns = [
    # Authentication
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User profile
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('password/change/', PasswordChangeView.as_view(), name='password-change'),
    
    # Households
    path('', include(router.urls)),
]
