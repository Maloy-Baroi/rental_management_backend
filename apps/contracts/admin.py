from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import RentalContract, RentalContractParticipant, RentalContractAuthor


class RentalContractParticipantInline(admin.TabularInline):
    """Inline admin for contract participants"""
    model = RentalContractParticipant
    extra = 1
    autocomplete_fields = ['household']


class RentalContractAuthorInline(admin.TabularInline):
    """Inline admin for contract authors"""
    model = RentalContractAuthor
    extra = 0
    autocomplete_fields = ['user']


@admin.register(RentalContract)
class RentalContractAdmin(admin.ModelAdmin):
    """Admin for RentalContract model"""

    list_display = [
        'contract_summary', 'unit', 'tenant_household', 'contract_from',
        'contract_to', 'rent_amount_at_contract', 'status_badge', 'created_at'
    ]
    list_filter = ['status', 'contract_from', 'contract_to', 'created_at']
    search_fields = [
        'unit__apartment_no', 'unit__property__house_name',
        'tenant_household__name', 'tenant_household__contact_phone'
    ]
    readonly_fields = ['created_at', 'updated_at', 'contract_duration']
    autocomplete_fields = ['unit', 'tenant_household', 'created_by']
    inlines = [RentalContractParticipantInline, RentalContractAuthorInline]
    date_hierarchy = 'contract_from'

    fieldsets = (
        ('Contract Parties', {
            'fields': ('unit', 'tenant_household'),
        }),
        ('Contract Period', {
            'fields': ('contract_from', 'contract_to', 'contract_duration'),
            'description': 'Contract start and end dates'
        }),
        ('Financial Terms', {
            'fields': ('rent_amount_at_contract', 'advance_paid_months', 'service_charge_at_contract'),
        }),
        ('Contract Status', {
            'fields': ('status', 'terminated_at', 'termination_reason'),
        }),
        ('Management', {
            'fields': ('created_by',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25
    actions = ['terminate_contracts', 'mark_as_expired']

    def contract_summary(self, obj):
        """Display contract summary"""
        return f"Contract #{obj.id}"
    contract_summary.short_description = 'Contract'

    def status_badge(self, obj):
        """Display status as colored badge"""
        colors = {
            'active': 'green',
            'terminated': 'red',
            'expired': 'orange'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; text-transform: uppercase;">{}</span>',
            color, obj.status
        )
    status_badge.short_description = 'Status'

    def contract_duration(self, obj):
        """Calculate and display contract duration"""
        if obj.contract_from and obj.contract_to:
            duration = (obj.contract_to - obj.contract_from).days
            months = duration // 30
            days = duration % 30
            return f"{months} months, {days} days"
        return "-"
    contract_duration.short_description = 'Duration'

    def terminate_contracts(self, request, queryset):
        """Terminate selected contracts"""
        count = 0
        for contract in queryset.filter(status='active'):
            contract.status = 'terminated'
            contract.terminated_at = timezone.now()
            contract.termination_reason = 'Terminated by admin'
            contract.save()
            count += 1
        self.message_user(request, f'{count} contract(s) terminated successfully.')
    terminate_contracts.short_description = "Terminate selected contracts"

    def mark_as_expired(self, request, queryset):
        """Mark contracts as expired"""
        count = queryset.filter(
            status='active',
            contract_to__lt=timezone.now().date()
        ).update(status='expired')
        self.message_user(request, f'{count} contract(s) marked as expired.')
    mark_as_expired.short_description = "Mark expired contracts"

    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related(
            'unit',
            'unit__property',
            'tenant_household',
            'created_by'
        )


@admin.register(RentalContractParticipant)
class RentalContractParticipantAdmin(admin.ModelAdmin):
    """Admin for RentalContractParticipant model"""

    list_display = ['contract', 'household', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = [
        'contract__unit__apartment_no',
        'household__name',
        'household__contact_phone'
    ]
    readonly_fields = ['created_at']
    autocomplete_fields = ['contract', 'household']

    fieldsets = (
        ('Participant Information', {
            'fields': ('contract', 'household', 'role'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25

    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('contract', 'household')


@admin.register(RentalContractAuthor)
class RentalContractAuthorAdmin(admin.ModelAdmin):
    """Admin for RentalContractAuthor model"""

    list_display = [
        'contract', 'user', 'role', 'can_approve',
        'can_terminate', 'can_renew', 'is_active_badge', 'created_at'
    ]
    list_filter = ['role', 'is_active', 'can_approve', 'can_terminate', 'can_renew', 'created_at']
    search_fields = [
        'contract__unit__apartment_no',
        'user__phone',
        'user__email'
    ]
    readonly_fields = ['created_at']
    autocomplete_fields = ['contract', 'user']

    fieldsets = (
        ('Author Information', {
            'fields': ('contract', 'user', 'role', 'is_active'),
        }),
        ('Permissions', {
            'fields': ('can_approve', 'can_terminate', 'can_renew'),
            'description': 'Define what actions this author can perform'
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25
    actions = ['activate_authors', 'deactivate_authors']

    def is_active_badge(self, obj):
        """Display active status as badge"""
        if obj.is_active:
            return format_html(
                '<span style="background-color: green; color: white; padding: 3px 10px; border-radius: 3px;">Active</span>'
            )
        else:
            return format_html(
                '<span style="background-color: red; color: white; padding: 3px 10px; border-radius: 3px;">Inactive</span>'
            )
    is_active_badge.short_description = 'Status'

    def activate_authors(self, request, queryset):
        """Activate selected authors"""
        count = queryset.update(is_active=True)
        self.message_user(request, f'{count} author(s) activated successfully.')
    activate_authors.short_description = "Activate selected authors"

    def deactivate_authors(self, request, queryset):
        """Deactivate selected authors"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} author(s) deactivated successfully.')
    deactivate_authors.short_description = "Deactivate selected authors"

    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('contract', 'user')

