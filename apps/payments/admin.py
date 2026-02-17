from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import Payment, PaymentWebhook


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin for Payment model"""

    list_display = [
        'payment_id', 'contract', 'payment_type', 'amount',
        'provider', 'status_badge', 'created_at'
    ]
    list_filter = ['status', 'payment_type', 'provider', 'created_at']
    search_fields = [
        'contract__unit__apartment_no',
        'contract__tenant_household__name',
        'provider_payment_id',
        'idempotency_key'
    ]
    readonly_fields = ['created_at', 'updated_at', 'idempotency_key']
    autocomplete_fields = ['contract', 'bill', 'received_by_user']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Payment Information', {
            'fields': ('contract', 'bill', 'amount', 'payment_type'),
        }),
        ('Provider Details', {
            'fields': ('provider', 'provider_payment_id', 'idempotency_key'),
        }),
        ('Payment Status', {
            'fields': ('status',),
        }),
        ('Manual Payment Info', {
            'fields': ('received_by_user',),
            'description': 'For cash or manual payments'
        }),
        ('Additional Information', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25
    actions = ['mark_as_succeeded', 'mark_as_failed', 'mark_as_refunded']

    def payment_id(self, obj):
        """Display payment ID"""
        return f"PAY-{obj.id}"
    payment_id.short_description = 'Payment ID'

    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            'pending': 'gray',
            'processing': 'blue',
            'succeeded': 'green',
            'failed': 'red',
            'refunded': 'orange'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; text-transform: uppercase;">{}</span>',
            color, obj.status
        )
    status_badge.short_description = 'Status'

    def mark_as_succeeded(self, request, queryset):
        """Mark payments as succeeded"""
        count = queryset.update(status='succeeded')
        self.message_user(request, f'{count} payment(s) marked as succeeded.')
    mark_as_succeeded.short_description = "Mark as succeeded"

    def mark_as_failed(self, request, queryset):
        """Mark payments as failed"""
        count = queryset.update(status='failed')
        self.message_user(request, f'{count} payment(s) marked as failed.')
    mark_as_failed.short_description = "Mark as failed"

    def mark_as_refunded(self, request, queryset):
        """Mark payments as refunded"""
        count = queryset.filter(status='succeeded').update(status='refunded')
        self.message_user(request, f'{count} payment(s) marked as refunded.')
    mark_as_refunded.short_description = "Mark as refunded"

    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related(
            'contract',
            'contract__unit',
            'contract__tenant_household',
            'bill',
            'received_by_user'
        )

    def changelist_view(self, request, extra_context=None):
        """Add summary statistics to changelist"""
        extra_context = extra_context or {}

        # Get filtered queryset
        cl = self.get_changelist_instance(request)
        queryset = cl.get_queryset(request)

        # Calculate statistics
        total_payments = queryset.count()
        total_amount = queryset.filter(status='succeeded').aggregate(Sum('amount'))['amount__sum'] or 0
        pending_payments = queryset.filter(status='pending').count()
        succeeded_payments = queryset.filter(status='succeeded').count()
        failed_payments = queryset.filter(status='failed').count()

        # Group by provider
        by_provider = queryset.values('provider').annotate(
            count=Count('id'),
            total=Sum('amount')
        ).order_by('-total')

        extra_context['total_payments'] = total_payments
        extra_context['total_amount'] = total_amount
        extra_context['pending_payments'] = pending_payments
        extra_context['succeeded_payments'] = succeeded_payments
        extra_context['failed_payments'] = failed_payments
        extra_context['by_provider'] = by_provider

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(PaymentWebhook)
class PaymentWebhookAdmin(admin.ModelAdmin):
    """Admin for PaymentWebhook model"""

    list_display = [
        'webhook_id', 'provider', 'event_type', 'event_id',
        'processed_badge', 'processed_at', 'created_at'
    ]
    list_filter = ['provider', 'event_type', 'processed', 'created_at']
    search_fields = ['event_id', 'event_type', 'provider']
    readonly_fields = ['created_at', 'payload']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Webhook Information', {
            'fields': ('provider', 'event_id', 'event_type'),
        }),
        ('Processing Status', {
            'fields': ('processed', 'processed_at', 'error_message'),
        }),
        ('Payload', {
            'fields': ('payload',),
            'classes': ('collapse',),
            'description': 'Raw webhook payload data'
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25
    actions = ['mark_as_processed', 'mark_as_unprocessed', 'retry_processing']

    def webhook_id(self, obj):
        """Display webhook ID"""
        return f"WHK-{obj.id}"
    webhook_id.short_description = 'Webhook ID'

    def processed_badge(self, obj):
        """Display processed status as badge"""
        if obj.processed:
            color = 'green'
            text = 'Processed'
        else:
            color = 'orange'
            text = 'Pending'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, text
        )
    processed_badge.short_description = 'Status'

    def mark_as_processed(self, request, queryset):
        """Mark webhooks as processed"""
        from django.utils import timezone
        count = queryset.update(processed=True, processed_at=timezone.now())
        self.message_user(request, f'{count} webhook(s) marked as processed.')
    mark_as_processed.short_description = "Mark as processed"

    def mark_as_unprocessed(self, request, queryset):
        """Mark webhooks as unprocessed"""
        count = queryset.update(processed=False, processed_at=None, error_message=None)
        self.message_user(request, f'{count} webhook(s) marked as unprocessed.')
    mark_as_unprocessed.short_description = "Mark as unprocessed"

    def retry_processing(self, request, queryset):
        """Retry processing failed webhooks"""
        count = queryset.filter(processed=False).update(
            error_message='Retrying...',
            processed_at=None
        )
        self.message_user(request, f'{count} webhook(s) queued for retry.')
    retry_processing.short_description = "Retry processing"

    def changelist_view(self, request, extra_context=None):
        """Add summary statistics to changelist"""
        extra_context = extra_context or {}

        # Get filtered queryset
        cl = self.get_changelist_instance(request)
        queryset = cl.get_queryset(request)

        # Calculate statistics
        total_webhooks = queryset.count()
        processed_webhooks = queryset.filter(processed=True).count()
        pending_webhooks = queryset.filter(processed=False).count()

        # Group by provider and event type
        by_provider = queryset.values('provider').annotate(count=Count('id')).order_by('-count')
        by_event_type = queryset.values('event_type').annotate(count=Count('id')).order_by('-count')[:10]

        extra_context['total_webhooks'] = total_webhooks
        extra_context['processed_webhooks'] = processed_webhooks
        extra_context['pending_webhooks'] = pending_webhooks
        extra_context['by_provider'] = by_provider
        extra_context['by_event_type'] = by_event_type

        return super().changelist_view(request, extra_context=extra_context)

