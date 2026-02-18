from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.utils import timezone

from .models import Bill
from .serializers import BillSerializer


@extend_schema_view(
    list=extend_schema(
        description="List all bills",
        summary="Get bills list",
        tags=['Billing']
    ),
    retrieve=extend_schema(
        description="Get a specific bill by ID",
        summary="Get bill detail",
        tags=['Billing']
    ),
    create=extend_schema(
        description="Create a new bill",
        summary="Create bill",
        tags=['Billing']
    ),
    update=extend_schema(
        description="Update a bill",
        summary="Update bill",
        tags=['Billing']
    ),
    partial_update=extend_schema(
        description="Partially update a bill",
        summary="Partial update bill",
        tags=['Billing']
    ),
    destroy=extend_schema(
        description="Delete a bill",
        summary="Delete bill",
        tags=['Billing']
    ),
)
class BillViewSet(viewsets.ModelViewSet):
    """ViewSet for Bill model"""

    queryset = Bill.objects.select_related(
        'contract',
        'contract__unit',
        'contract__tenant_household',
        'utility_type'
    ).prefetch_related('payments')
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['contract', 'status', 'utility_type', 'billing_month']
    search_fields = ['contract__unit__unit_no', 'billing_month', 'external_ref']
    ordering_fields = ['created_at', 'billing_month', 'due_date', 'amount']
    ordering = ['-billing_month', '-due_date']

    @extend_schema(
        description="Get pending bills",
        summary="Get pending bills",
        tags=['Billing']
    )
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending bills"""
        bills = self.queryset.filter(status='pending')
        serializer = self.get_serializer(bills, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Get overdue bills",
        summary="Get overdue bills",
        tags=['Billing']
    )
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get all overdue bills"""
        bills = self.queryset.filter(status='pending', due_date__lt=timezone.now().date())
        serializer = self.get_serializer(bills, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Mark bill as paid",
        summary="Mark bill as paid",
        tags=['Billing']
    )
    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark a bill as paid"""
        bill = self.get_object()

        if bill.status == 'paid':
            return Response(
                {'error': 'Bill is already marked as paid'},
                status=status.HTTP_400_BAD_REQUEST
            )

        bill.status = 'paid'
        bill.paid_on = timezone.now()
        bill.save()

        serializer = self.get_serializer(bill)
        return Response(serializer.data)

