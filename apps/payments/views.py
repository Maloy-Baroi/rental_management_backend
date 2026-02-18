from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models import Sum

from .models import Payment
from .serializers import PaymentSerializer


@extend_schema_view(
    list=extend_schema(
        description="List all payments",
        summary="Get payments list",
        tags=['Payments']
    ),
    retrieve=extend_schema(
        description="Get a specific payment by ID",
        summary="Get payment detail",
        tags=['Payments']
    ),
    create=extend_schema(
        description="Create a new payment",
        summary="Create payment",
        tags=['Payments']
    ),
    update=extend_schema(
        description="Update a payment",
        summary="Update payment",
        tags=['Payments']
    ),
    partial_update=extend_schema(
        description="Partially update a payment",
        summary="Partial update payment",
        tags=['Payments']
    ),
    destroy=extend_schema(
        description="Delete a payment",
        summary="Delete payment",
        tags=['Payments']
    ),
)
class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Payment model"""

    queryset = Payment.objects.select_related(
        'contract',
        'contract__unit',
        'bill',
        'received_by_user'
    )
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['contract', 'bill', 'payment_type', 'provider', 'status']
    search_fields = ['provider_payment_id', 'idempotency_key', 'contract__unit__unit_no']
    ordering_fields = ['created_at', 'amount', 'status']
    ordering = ['-created_at']

    @extend_schema(
        description="Get successful payments",
        summary="Get successful payments",
        tags=['Payments']
    )
    @action(detail=False, methods=['get'])
    def successful(self, request):
        """Get all successful payments"""
        payments = self.queryset.filter(status='succeeded')
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Get pending payments",
        summary="Get pending payments",
        tags=['Payments']
    )
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending payments"""
        payments = self.queryset.filter(status='pending')
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Get payment statistics",
        summary="Get payment statistics",
        tags=['Payments']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get payment statistics"""
        total_amount = self.queryset.filter(status='succeeded').aggregate(
            total=Sum('amount')
        )['total'] or 0

        stats = {
            'total_payments': self.queryset.count(),
            'successful_payments': self.queryset.filter(status='succeeded').count(),
            'pending_payments': self.queryset.filter(status='pending').count(),
            'failed_payments': self.queryset.filter(status='failed').count(),
            'total_amount_collected': float(total_amount),
        }

        return Response(stats)

