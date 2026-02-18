from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.utils import timezone

from .models import RentalContract, RentalContractParticipant
from .serializers import RentalContractSerializer, RentalContractParticipantSerializer


@extend_schema_view(
    list=extend_schema(
        description="List all rental contracts",
        summary="Get rental contracts list",
        tags=['Contracts']
    ),
    retrieve=extend_schema(
        description="Get a specific rental contract by ID",
        summary="Get rental contract detail",
        tags=['Contracts']
    ),
    create=extend_schema(
        description="Create a new rental contract",
        summary="Create rental contract",
        tags=['Contracts']
    ),
    update=extend_schema(
        description="Update a rental contract",
        summary="Update rental contract",
        tags=['Contracts']
    ),
    partial_update=extend_schema(
        description="Partially update a rental contract",
        summary="Partial update rental contract",
        tags=['Contracts']
    ),
    destroy=extend_schema(
        description="Delete a rental contract",
        summary="Delete rental contract",
        tags=['Contracts']
    ),
)
class RentalContractViewSet(viewsets.ModelViewSet):
    """ViewSet for RentalContract model"""

    queryset = RentalContract.objects.select_related(
        'unit',
        'unit__property',
        'tenant_household',
        'created_by'
    ).prefetch_related('participants')
    serializer_class = RentalContractSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['unit', 'tenant_household', 'status']
    search_fields = ['unit__unit_no', 'tenant_household__name']
    ordering_fields = ['created_at', 'contract_from', 'contract_to']
    ordering = ['-created_at']

    @extend_schema(
        description="Terminate a rental contract",
        summary="Terminate contract",
        tags=['Contracts'],
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'termination_reason': {'type': 'string', 'description': 'Reason for termination'}
                },
                'required': ['termination_reason']
            }
        }
    )
    @action(detail=True, methods=['post'])
    def terminate(self, request, pk=None):
        """Terminate a rental contract"""
        contract = self.get_object()

        if contract.status != 'active':
            return Response(
                {'error': 'Only active contracts can be terminated'},
                status=status.HTTP_400_BAD_REQUEST
            )

        contract.status = 'terminated'
        contract.terminated_at = timezone.now()
        contract.termination_reason = request.data.get('termination_reason', '')
        contract.save()

        serializer = self.get_serializer(contract)
        return Response(serializer.data)

    @extend_schema(
        description="Get active rental contracts",
        summary="Get active contracts",
        tags=['Contracts']
    )
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active contracts"""
        contracts = self.queryset.filter(status='active')
        serializer = self.get_serializer(contracts, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Get participants for a contract",
        summary="Get contract participants",
        tags=['Contracts'],
        responses={200: RentalContractParticipantSerializer(many=True)}
    )
    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        """Get all participants for a contract"""
        contract = self.get_object()
        participants = contract.participants.all()
        serializer = RentalContractParticipantSerializer(participants, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(
        description="List all rental contract participants",
        summary="Get participants list",
        tags=['Contracts']
    ),
    retrieve=extend_schema(
        description="Get a specific participant by ID",
        summary="Get participant detail",
        tags=['Contracts']
    ),
    create=extend_schema(
        description="Add a new participant to a contract",
        summary="Create participant",
        tags=['Contracts']
    ),
    update=extend_schema(
        description="Update a participant",
        summary="Update participant",
        tags=['Contracts']
    ),
    partial_update=extend_schema(
        description="Partially update a participant",
        summary="Partial update participant",
        tags=['Contracts']
    ),
    destroy=extend_schema(
        description="Remove a participant from a contract",
        summary="Delete participant",
        tags=['Contracts']
    ),
)
class RentalContractParticipantViewSet(viewsets.ModelViewSet):
    """ViewSet for RentalContractParticipant model"""

    queryset = RentalContractParticipant.objects.select_related(
        'contract',
        'household_member'
    )
    serializer_class = RentalContractParticipantSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['contract', 'role']
    ordering_fields = ['created_at', 'role']
    ordering = ['-created_at']

