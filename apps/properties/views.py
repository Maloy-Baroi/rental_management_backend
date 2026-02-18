from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Location, Property, Unit, UtilityType
from .serializers import (
    LocationSerializer,
    PropertySerializer,
    UnitSerializer,
    UtilityTypeSerializer
)


@extend_schema_view(
    list=extend_schema(
        description="List all locations",
        summary="Get locations list",
        tags=['Properties']
    ),
    retrieve=extend_schema(
        description="Get a specific location by ID",
        summary="Get location detail",
        tags=['Properties']
    ),
    create=extend_schema(
        description="Create a new location",
        summary="Create location",
        tags=['Properties']
    ),
    update=extend_schema(
        description="Update a location",
        summary="Update location",
        tags=['Properties']
    ),
    partial_update=extend_schema(
        description="Partially update a location",
        summary="Partial update location",
        tags=['Properties']
    ),
    destroy=extend_schema(
        description="Delete a location",
        summary="Delete location",
        tags=['Properties']
    ),
)
class LocationViewSet(viewsets.ModelViewSet):
    """ViewSet for Location model"""

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['district', 'division', 'country']
    search_fields = ['area_name', 'district', 'division', 'upazila_or_thana']
    ordering_fields = ['created_at', 'district']
    ordering = ['-created_at']


@extend_schema_view(
    list=extend_schema(
        description="List all properties",
        summary="Get properties list",
        tags=['Properties']
    ),
    retrieve=extend_schema(
        description="Get a specific property by ID",
        summary="Get property detail",
        tags=['Properties']
    ),
    create=extend_schema(
        description="Create a new property",
        summary="Create property",
        tags=['Properties']
    ),
    update=extend_schema(
        description="Update a property",
        summary="Update property",
        tags=['Properties']
    ),
    partial_update=extend_schema(
        description="Partially update a property",
        summary="Partial update property",
        tags=['Properties']
    ),
    destroy=extend_schema(
        description="Delete a property",
        summary="Delete property",
        tags=['Properties']
    ),
)
class PropertyViewSet(viewsets.ModelViewSet):
    """ViewSet for Property model"""

    queryset = Property.objects.select_related('location', 'created_by').prefetch_related('units')
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'has_lift', 'has_parking', 'has_security_guard']
    search_fields = ['house_name', 'location__district', 'location__area_name']
    ordering_fields = ['created_at', 'house_name', 'total_floors']
    ordering = ['-created_at']

    @extend_schema(
        description="Get units for a specific property",
        summary="Get property units",
        tags=['Properties'],
        responses={200: UnitSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def units(self, request, pk=None):
        """Get all units for a property"""
        property_obj = self.get_object()
        units = property_obj.units.all()
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        description="List all units",
        summary="Get units list",
        tags=['Properties']
    ),
    retrieve=extend_schema(
        description="Get a specific unit by ID",
        summary="Get unit detail",
        tags=['Properties']
    ),
    create=extend_schema(
        description="Create a new unit",
        summary="Create unit",
        tags=['Properties']
    ),
    update=extend_schema(
        description="Update a unit",
        summary="Update unit",
        tags=['Properties']
    ),
    partial_update=extend_schema(
        description="Partially update a unit",
        summary="Partial update unit",
        tags=['Properties']
    ),
    destroy=extend_schema(
        description="Delete a unit",
        summary="Delete unit",
        tags=['Properties']
    ),
)
class UnitViewSet(viewsets.ModelViewSet):
    """ViewSet for Unit model"""

    queryset = Unit.objects.select_related('property', 'property__location')
    serializer_class = UnitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property', 'floor_no', 'facing_direction']
    search_fields = ['apartment_no', 'property__house_name']
    ordering_fields = ['created_at', 'floor_no']
    ordering = ['-created_at']

    @extend_schema(
        description="Get available units",
        summary="Get available units",
        tags=['Properties'],
        parameters=[
            OpenApiParameter(
                name='available',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Filter by availability'
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available units"""
        units = self.queryset.filter(is_available=True)
        serializer = self.get_serializer(units, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        description="List all utility types",
        summary="Get utility types list",
        tags=['Properties']
    ),
    retrieve=extend_schema(
        description="Get a specific utility type by ID",
        summary="Get utility type detail",
        tags=['Properties']
    ),
    create=extend_schema(
        description="Create a new utility type",
        summary="Create utility type",
        tags=['Properties']
    ),
    update=extend_schema(
        description="Update a utility type",
        summary="Update utility type",
        tags=['Properties']
    ),
    partial_update=extend_schema(
        description="Partially update a utility type",
        summary="Partial update utility type",
        tags=['Properties']
    ),
    destroy=extend_schema(
        description="Delete a utility type",
        summary="Delete utility type",
        tags=['Properties']
    ),
)
class UtilityTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for UtilityType model"""

    queryset = UtilityType.objects.all()
    serializer_class = UtilityTypeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

