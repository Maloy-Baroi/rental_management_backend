from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.db.models import Count

from .models import AuditLog
from .serializers import AuditLogSerializer


@extend_schema_view(
    list=extend_schema(
        description="List all audit logs",
        summary="Get audit logs list",
        tags=['Audit']
    ),
    retrieve=extend_schema(
        description="Get a specific audit log by ID",
        summary="Get audit log detail",
        tags=['Audit']
    ),
)
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for AuditLog model (Read-only)

    Audit logs are automatically created by the system and cannot be modified.
    This ViewSet provides read-only access to view audit trail.
    """

    queryset = AuditLog.objects.select_related('actor_user', 'content_type')
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['entity_type', 'action', 'actor_user']
    search_fields = ['entity_type', 'entity_id', 'actor_user__phone', 'actor_user__email']
    ordering_fields = ['created_at', 'action', 'entity_type']
    ordering = ['-created_at']

    @extend_schema(
        description="Get audit logs for a specific entity",
        summary="Get entity audit logs",
        tags=['Audit'],
        parameters=[
            OpenApiParameter(
                name='entity_type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Type of entity (e.g., RentalContract, Payment)',
                required=True
            ),
            OpenApiParameter(
                name='entity_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='ID of the entity',
                required=True
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def by_entity(self, request):
        """Get all audit logs for a specific entity"""
        entity_type = request.query_params.get('entity_type')
        entity_id = request.query_params.get('entity_id')

        if not entity_type or not entity_id:
            return Response(
                {'error': 'Both entity_type and entity_id parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        logs = self.queryset.filter(entity_type=entity_type, entity_id=entity_id)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Get audit logs for a specific user",
        summary="Get user audit logs",
        tags=['Audit'],
        parameters=[
            OpenApiParameter(
                name='user_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='ID of the user',
                required=True
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get all audit logs for a specific user"""
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        logs = self.queryset.filter(actor_user_id=user_id)
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Get audit log statistics",
        summary="Get audit statistics",
        tags=['Audit']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get audit log statistics"""
        # Actions breakdown
        actions_stats = self.queryset.values('action').annotate(
            count=Count('id')
        ).order_by('-count')

        # Entity types breakdown
        entity_stats = self.queryset.values('entity_type').annotate(
            count=Count('id')
        ).order_by('-count')

        # Top actors
        top_actors = self.queryset.filter(
            actor_user__isnull=False
        ).values(
            'actor_user__id',
            'actor_user__phone',
            'actor_user__email'
        ).annotate(
            action_count=Count('id')
        ).order_by('-action_count')[:10]

        stats = {
            'total_logs': self.queryset.count(),
            'actions_breakdown': list(actions_stats),
            'entity_types_breakdown': list(entity_stats),
            'top_actors': list(top_actors),
        }

        return Response(stats)

    @extend_schema(
        description="Get recent audit logs",
        summary="Get recent audit logs",
        tags=['Audit'],
        parameters=[
            OpenApiParameter(
                name='limit',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Number of recent logs to return (default: 50)',
                required=False
            ),
        ]
    )
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Get recent audit logs"""
        limit = int(request.query_params.get('limit', 50))
        logs = self.queryset[:limit]
        serializer = self.get_serializer(logs, many=True)
        return Response(serializer.data)

