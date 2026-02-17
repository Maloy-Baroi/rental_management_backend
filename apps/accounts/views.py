from rest_framework import viewsets, generics, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db import connection

from .models import Household
from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    HouseholdSerializer,
    HouseholdCreateSerializer,
    PasswordChangeSerializer
)

User = get_user_model()


class HealthCheckView(views.APIView):
    """Health check endpoint"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            db_status = "healthy"
        except Exception as e:
            db_status = f"unhealthy: {str(e)}"
        
        return Response({
            'status': 'healthy' if db_status == 'healthy' else 'unhealthy',
            'database': db_status,
        })


@extend_schema_view(
    post=extend_schema(
        summary='Register new user',
        description='Create a new user account with phone and password',
    )
)
class UserRegistrationView(generics.CreateAPIView):
    """User registration endpoint"""
    
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        summary='Get user profile',
        description='Retrieve authenticated user profile',
    ),
    put=extend_schema(
        summary='Update user profile',
        description='Update authenticated user profile',
    ),
    patch=extend_schema(
        summary='Partial update user profile',
        description='Partially update authenticated user profile',
    ),
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile management"""
    
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@extend_schema_view(
    post=extend_schema(
        summary='Change password',
        description='Change user password',
    )
)
class PasswordChangeView(generics.GenericAPIView):
    """Password change endpoint"""
    
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'message': 'Password changed successfully'
        }, status=status.HTTP_200_OK)


@extend_schema_view(
    list=extend_schema(
        summary='List households',
        description='List all households created by authenticated user',
    ),
    create=extend_schema(
        summary='Create household',
        description='Create new household',
    ),
    retrieve=extend_schema(
        summary='Get household',
        description='Retrieve household details',
    ),
    update=extend_schema(
        summary='Update household',
        description='Update household details',
    ),
    partial_update=extend_schema(
        summary='Partial update household',
        description='Partially update household details',
    ),
    destroy=extend_schema(
        summary='Delete household',
        description='Delete household',
    ),
)
class HouseholdViewSet(viewsets.ModelViewSet):
    """Household CRUD operations"""
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Household.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return HouseholdCreateSerializer
        return HouseholdSerializer
