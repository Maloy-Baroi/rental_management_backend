from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import User, Household


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for custom User model"""

    list_display = ['phone', 'email', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'status_badge']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'is_deleted', 'created_at']
    search_fields = ['phone', 'email']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at', 'last_login']

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        (_('Personal info'), {'fields': ('email',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_deleted', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'email', 'password1', 'password2', 'is_staff', 'is_superuser'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions',)

    def status_badge(self, obj):
        """Display status as colored badge"""
        if obj.is_deleted:
            color = 'red'
            status = 'Deleted'
        elif obj.is_active:
            color = 'green'
            status = 'Active'
        else:
            color = 'orange'
            status = 'Inactive'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, status
        )
    status_badge.short_description = 'Status'

    actions = ['activate_users', 'deactivate_users', 'soft_delete_users']

    def activate_users(self, request, queryset):
        """Activate selected users"""
        count = queryset.update(is_active=True, is_deleted=False)
        self.message_user(request, f'{count} user(s) activated successfully.')
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        """Deactivate selected users"""
        count = queryset.update(is_active=False)
        self.message_user(request, f'{count} user(s) deactivated successfully.')
    deactivate_users.short_description = "Deactivate selected users"

    def soft_delete_users(self, request, queryset):
        """Soft delete selected users"""
        count = 0
        for user in queryset:
            user.soft_delete()
            count += 1
        self.message_user(request, f'{count} user(s) soft deleted successfully.')
    soft_delete_users.short_description = "Soft delete selected users"


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    """Admin for Household model"""

    list_display = ['name', 'contact_phone', 'user', 'date_of_birth', 'nid', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'contact_phone', 'nid', 'user__phone', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['user']

    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'date_of_birth', 'nid'),
            'description': 'Basic personal information of the household member'
        }),
        ('Contact Information', {
            'fields': ('contact_phone',)
        }),
        ('Association', {
            'fields': ('user',),
            'description': 'User who created this household'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25

    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('user')

