from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Location, Property, Unit, UnitRoomSummary,
    RentalTerms, UnitPolicy, UtilityType, UnitUtility
)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Admin for Location model"""

    list_display = ['location_summary', 'district', 'division', 'country', 'created_at']
    list_filter = ['division', 'district', 'country', 'created_at']
    search_fields = ['area_name', 'village', 'district', 'division', 'upazila_or_thana']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Location Details', {
            'fields': ('area_name', 'village', 'ward', 'zone_or_union'),
        }),
        ('Administrative Division', {
            'fields': ('city_corporation', 'upazila_or_thana', 'district', 'division', 'country'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25

    def location_summary(self, obj):
        """Display formatted location summary"""
        return str(obj)
    location_summary.short_description = 'Location'


class UnitInline(admin.TabularInline):
    """Inline admin for units within property"""
    model = Unit
    extra = 0
    fields = ['apartment_no', 'floor_no', 'facing_direction', 'size_sqft']
    show_change_link = True


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """Admin for Property model"""

    list_display = ['house_name', 'location', 'total_floors', 'amenities_summary', 'created_by', 'created_at']
    list_filter = ['has_lift', 'has_security_guard', 'has_parking', 'is_tiled', 'created_at']
    search_fields = ['house_name', 'location__district', 'location__division', 'created_by__phone']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['location', 'created_by']
    inlines = [UnitInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('house_name', 'location', 'age_of_building', 'total_floors'),
        }),
        ('Amenities', {
            'fields': ('has_lift', 'has_security_guard', 'has_parking', 'is_tiled'),
        }),
        ('Media', {
            'fields': ('photos',),
            'description': 'Upload property photos (JSON format)'
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

    def amenities_summary(self, obj):
        """Display amenities as badges"""
        amenities = []
        if obj.has_lift:
            amenities.append('<span class="badge badge-primary">Lift</span>')
        if obj.has_security_guard:
            amenities.append('<span class="badge badge-success">Security</span>')
        if obj.has_parking:
            amenities.append('<span class="badge badge-info">Parking</span>')
        if obj.is_tiled:
            amenities.append('<span class="badge badge-secondary">Tiled</span>')
        return format_html(' '.join(amenities)) if amenities else '-'
    amenities_summary.short_description = 'Amenities'

    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('location', 'created_by')


class UnitRoomSummaryInline(admin.StackedInline):
    """Inline admin for unit room summary"""
    model = UnitRoomSummary
    can_delete = False
    verbose_name_plural = 'Room Summary'


class RentalTermsInline(admin.StackedInline):
    """Inline admin for rental terms"""
    model = RentalTerms
    can_delete = False
    verbose_name_plural = 'Rental Terms'


class UnitPolicyInline(admin.StackedInline):
    """Inline admin for unit policy"""
    model = UnitPolicy
    can_delete = False
    verbose_name_plural = 'Unit Policy'


class UnitUtilityInline(admin.TabularInline):
    """Inline admin for unit utilities"""
    model = UnitUtility
    extra = 1


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    """Admin for Unit model"""

    list_display = ['unit_name', 'property', 'floor_no', 'facing_direction', 'size_sqft', 'availability_badge', 'created_at']
    list_filter = ['property', 'floor_no', 'facing_direction', 'created_at']
    search_fields = ['apartment_no', 'property__house_name', 'property__location__district']
    readonly_fields = ['created_at', 'updated_at', 'is_available']
    autocomplete_fields = ['property']
    inlines = [UnitRoomSummaryInline, RentalTermsInline, UnitPolicyInline, UnitUtilityInline]

    fieldsets = (
        ('Unit Information', {
            'fields': ('property', 'apartment_no', 'floor_no', 'facing_direction', 'size_sqft'),
        }),
        ('Availability', {
            'fields': ('is_available',),
            'description': 'Check if unit is currently available for rent'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25

    def unit_name(self, obj):
        """Display unit name"""
        return str(obj)
    unit_name.short_description = 'Unit'

    def availability_badge(self, obj):
        """Display availability status"""
        if obj.is_available:
            return format_html(
                '<span style="background-color: green; color: white; padding: 3px 10px; border-radius: 3px;">Available</span>'
            )
        else:
            return format_html(
                '<span style="background-color: red; color: white; padding: 3px 10px; border-radius: 3px;">Occupied</span>'
            )
    availability_badge.short_description = 'Availability'

    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('property', 'property__location')


@admin.register(UnitRoomSummary)
class UnitRoomSummaryAdmin(admin.ModelAdmin):
    """Admin for UnitRoomSummary model"""

    list_display = ['unit', 'bedrooms', 'master_bedrooms', 'bathrooms', 'attached_baths', 'kitchens', 'balconies', 'has_separate_dining']
    list_filter = ['bedrooms', 'bathrooms', 'has_separate_dining']
    search_fields = ['unit__apartment_no', 'unit__property__house_name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['unit']

    fieldsets = (
        ('Bedrooms', {
            'fields': ('bedrooms', 'master_bedrooms'),
        }),
        ('Bathrooms', {
            'fields': ('bathrooms', 'attached_baths', 'common_baths'),
        }),
        ('Other Rooms', {
            'fields': ('kitchens', 'balconies', 'has_separate_dining'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25


@admin.register(RentalTerms)
class RentalTermsAdmin(admin.ModelAdmin):
    """Admin for RentalTerms model"""

    list_display = ['unit', 'asking_rent', 'minimum_rent', 'advance_months', 'service_charge', 'payment_due_day']
    list_filter = ['advance_months', 'payment_due_day']
    search_fields = ['unit__apartment_no', 'unit__property__house_name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['unit']

    fieldsets = (
        ('Rent Information', {
            'fields': ('asking_rent', 'minimum_rent', 'advance_months'),
        }),
        ('Additional Charges', {
            'fields': ('service_charge',),
        }),
        ('Payment Terms', {
            'fields': ('payment_due_day',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25


@admin.register(UnitPolicy)
class UnitPolicyAdmin(admin.ModelAdmin):
    """Admin for UnitPolicy model"""

    list_display = [
        'unit', 'pets_allowed', 'bachelor_allowed', 'sublet_allowed',
        'gender_restricted', 'roof_access', 'ac_installation_allowed'
    ]
    list_filter = [
        'pets_allowed', 'bachelor_allowed', 'sublet_allowed',
        'gender_restricted', 'roof_access', 'ac_installation_allowed'
    ]
    search_fields = ['unit__apartment_no', 'unit__property__house_name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['unit']

    fieldsets = (
        ('General Policies', {
            'fields': ('pets_allowed', 'bachelor_allowed', 'sublet_allowed', 'gender_restricted'),
        }),
        ('Property Access', {
            'fields': ('roof_access', 'roof_gardening_allowed', 'house_gardening_allowed'),
        }),
        ('Modifications', {
            'fields': ('ac_installation_allowed',),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25


@admin.register(UtilityType)
class UtilityTypeAdmin(admin.ModelAdmin):
    """Admin for UtilityType model"""

    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']


@admin.register(UnitUtility)
class UnitUtilityAdmin(admin.ModelAdmin):
    """Admin for UnitUtility model"""

    list_display = ['unit', 'utility_type', 'billing_type', 'is_included_in_rent', 'created_at']
    list_filter = ['utility_type', 'billing_type', 'is_included_in_rent']
    search_fields = ['unit__apartment_no', 'unit__property__house_name', 'utility_type__name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['unit', 'utility_type']

    fieldsets = (
        ('Utility Information', {
            'fields': ('unit', 'utility_type', 'billing_type', 'is_included_in_rent'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_per_page = 25

    def get_queryset(self, request):
        """Optimize queryset"""
        qs = super().get_queryset(request)
        return qs.select_related('unit', 'unit__property', 'utility_type')

