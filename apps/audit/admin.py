from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Admin for AuditLog model"""

    list_display = [
        'log_id', 'entity_type', 'entity_id', 'action_badge',
        'actor_user', 'ip_address', 'created_at'
    ]
    list_filter = ['action', 'entity_type', 'created_at']
    search_fields = [
        'entity_type', 'entity_id', 'actor_user__phone',
        'actor_user__email', 'ip_address'
    ]
    readonly_fields = ['created_at', 'formatted_data', 'content_object_link']
    autocomplete_fields = ['actor_user']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Entity Information', {
            'fields': ('entity_type', 'entity_id', 'content_object_link'),
        }),
        ('Action Details', {
            'fields': ('action', 'formatted_data'),
        }),
        ('Actor Information', {
            'fields': ('actor_user', 'ip_address', 'user_agent'),
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 50

    def has_add_permission(self, request):
        """Disable manual creation of audit logs"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable deletion of audit logs for data integrity"""
        return False

    def log_id(self, obj):
        """Display log ID"""
        return f"LOG-{obj.id}"
    log_id.short_description = 'Log ID'

    def action_badge(self, obj):
        """Display action as colored badge"""
        colors = {
            'create': 'green',
            'update': 'blue',
            'delete': 'red',
            'approve': 'purple',
            'reject': 'orange',
            'terminate': 'red',
            'renew': 'green',
            'payment': 'teal',
            'refund': 'orange'
        }
        color = colors.get(obj.action, 'gray')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; text-transform: uppercase;">{}</span>',
            color, obj.action
        )
    action_badge.short_description = 'Action'

    def formatted_data(self, obj):
        """Display formatted JSON data"""
        import json
        try:
            formatted = json.dumps(obj.data, indent=2)
            return format_html('<pre style="background: #f4f4f4; padding: 10px; border-radius: 5px;">{}</pre>', formatted)
        except:
            return obj.data
    formatted_data.short_description = 'Data Snapshot'

    def content_object_link(self, obj):
        """Display link to content object if available"""
        if obj.content_object:
            from django.urls import reverse
            from django.contrib.contenttypes.models import ContentType

            ct = ContentType.objects.get_for_model(obj.content_object)
            url = reverse(
                f'admin:{ct.app_label}_{ct.model}_change',
                args=[obj.content_object.pk]
            )
            return format_html('<a href="{}">{}</a>', url, obj.content_object)
        return '-'
    content_object_link.short_description = 'Related Object'

    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('actor_user', 'content_type')

    def changelist_view(self, request, extra_context=None):
        """Add summary statistics to changelist"""
        extra_context = extra_context or {}

        # Get filtered queryset
        cl = self.get_changelist_instance(request)
        queryset = cl.get_queryset(request)

        # Calculate statistics
        total_logs = queryset.count()

        # Group by action
        by_action = queryset.values('action').annotate(count=Count('id')).order_by('-count')

        # Group by entity type
        by_entity = queryset.values('entity_type').annotate(count=Count('id')).order_by('-count')[:10]

        # Top actors
        top_actors = queryset.filter(
            actor_user__isnull=False
        ).values(
            'actor_user__phone', 'actor_user__email'
        ).annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        extra_context['total_logs'] = total_logs
        extra_context['by_action'] = by_action
        extra_context['by_entity'] = by_entity
        extra_context['top_actors'] = top_actors

        return super().changelist_view(request, extra_context=extra_context)

