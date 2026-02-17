from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Sum
from .models import Bill


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    """Admin for Bill model"""

    list_display = [
        'bill_id', 'contract', 'bill_type', 'amount', 'billing_month',
        'due_date', 'status_badge', 'payment_progress', 'created_at'
    ]
    list_filter = ['status', 'billing_month', 'due_date', 'utility_type', 'created_at']
    search_fields = [
        'contract__unit__apartment_no',
        'contract__tenant_household__name',
        'external_ref',
        'billing_month'
    ]
    readonly_fields = ['created_at', 'updated_at', 'is_overdue', 'amount_paid', 'amount_remaining']
    autocomplete_fields = ['contract', 'utility_type']
    date_hierarchy = 'due_date'

    fieldsets = (
        ('Bill Information', {
            'fields': ('contract', 'utility_type', 'amount', 'billing_month'),
        }),
        ('Payment Details', {
            'fields': ('due_date', 'paid_on', 'status', 'external_ref'),
        }),
        ('Payment Summary', {
            'fields': ('is_overdue', 'amount_paid', 'amount_remaining'),
            'classes': ('collapse',),
            'description': 'Calculated payment information'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25
    actions = ['mark_as_paid', 'mark_as_overdue', 'mark_as_pending']

    def bill_id(self, obj):
        """Display bill ID"""
        return f"Bill #{obj.id}"
    bill_id.short_description = 'Bill ID'

    def bill_type(self, obj):
        """Display bill type"""
        if obj.utility_type:
            return obj.utility_type.name
        return "Rent"
    bill_type.short_description = 'Type'

    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            'pending': 'orange',
            'paid': 'green',
            'overdue': 'red',
            'partial': 'blue'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; text-transform: uppercase;">{}</span>',
            color, obj.status
        )
    status_badge.short_description = 'Status'

    def payment_progress(self, obj):
        """Display payment progress bar"""
        if obj.amount > 0:
            percentage = (obj.amount_paid / obj.amount) * 100
            color = 'green' if percentage == 100 else ('orange' if percentage > 0 else 'red')
            return format_html(
                '<div style="width: 100px; background-color: #f0f0f0; border-radius: 3px;">'
                '<div style="width: {}%; background-color: {}; color: white; text-align: center; border-radius: 3px; padding: 2px;">{:.0f}%</div>'
                '</div>',
                percentage, color, percentage
            )
        return "-"
    payment_progress.short_description = 'Payment Progress'

    def mark_as_paid(self, request, queryset):
        """Mark bills as paid"""
        count = queryset.update(
            status='paid',
            paid_on=timezone.now()
        )
        self.message_user(request, f'{count} bill(s) marked as paid.')
    mark_as_paid.short_description = "Mark as paid"

    def mark_as_overdue(self, request, queryset):
        """Mark bills as overdue"""
        count = queryset.filter(
            status='pending',
            due_date__lt=timezone.now().date()
        ).update(status='overdue')
        self.message_user(request, f'{count} bill(s) marked as overdue.')
    mark_as_overdue.short_description = "Mark as overdue"

    def mark_as_pending(self, request, queryset):
        """Mark bills as pending"""
        count = queryset.update(status='pending', paid_on=None)
        self.message_user(request, f'{count} bill(s) marked as pending.')
    mark_as_pending.short_description = "Mark as pending"

    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related(
            'contract',
            'contract__unit',
            'contract__tenant_household',
            'utility_type'
        )

    def changelist_view(self, request, extra_context=None):
        """Add summary statistics to changelist"""
        extra_context = extra_context or {}

        # Get filtered queryset
        cl = self.get_changelist_instance(request)
        queryset = cl.get_queryset(request)

        # Calculate statistics
        total_bills = queryset.count()
        total_amount = queryset.aggregate(Sum('amount'))['amount__sum'] or 0
        paid_bills = queryset.filter(status='paid').count()
        overdue_bills = queryset.filter(status='overdue').count()

        extra_context['total_bills'] = total_bills
        extra_context['total_amount'] = total_amount
        extra_context['paid_bills'] = paid_bills
        extra_context['overdue_bills'] = overdue_bills

        return super().changelist_view(request, extra_context=extra_context)

