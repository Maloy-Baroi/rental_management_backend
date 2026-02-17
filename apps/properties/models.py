import builtins
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

User = get_user_model()


class Location(models.Model):
    """Location/Address information"""
    
    area_name = models.CharField(max_length=255, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    ward = models.CharField(max_length=100, null=True, blank=True)
    zone_or_union = models.CharField(max_length=255, null=True, blank=True)
    city_corporation = models.CharField(max_length=255, null=True, blank=True)
    upazila_or_thana = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255)
    division = models.CharField(max_length=255)
    country = models.CharField(max_length=100, default='Bangladesh')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'locations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['district', 'division']),
            models.Index(fields=['upazila_or_thana']),
        ]
    
    def __str__(self):
        parts = [
            self.area_name,
            self.upazila_or_thana,
            self.district,
            self.division
        ]
        return ', '.join(filter(None, parts))


class Property(models.Model):
    """Property information"""
    
    location = models.ForeignKey(
        Location,
        on_delete=models.PROTECT,
        related_name='properties'
    )
    house_name = models.CharField(max_length=255)
    age_of_building = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    total_floors = models.IntegerField(validators=[MinValueValidator(1)])
    has_lift = models.BooleanField(default=False)
    has_security_guard = models.BooleanField(default=False)
    has_parking = models.BooleanField(default=False)
    is_tiled = models.BooleanField(default=True)
    photos = models.JSONField(default=list, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='properties_created'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'properties'
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['location', 'created_at']),
            models.Index(fields=['created_by']),
        ]
    
    def __str__(self):
        return f'{self.house_name} - {self.location.district}'


class Unit(models.Model):
    """Property unit/apartment"""
    
    FACING_CHOICES = [
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
        ('north_east', 'North-East'),
        ('north_west', 'North-West'),
        ('south_east', 'South-East'),
        ('south_west', 'South-West'),
    ]
    
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='units'
    )
    apartment_no = models.CharField(max_length=50)
    floor_no = models.IntegerField(validators=[MinValueValidator(0)])
    facing_direction = models.CharField(max_length=20, choices=FACING_CHOICES)
    size_sqft = models.IntegerField(validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'units'
        ordering = ['property', 'floor_no', 'apartment_no']
        unique_together = [['property', 'apartment_no']]
        indexes = [
            models.Index(fields=['property', 'floor_no']),
        ]
    
    def __str__(self):
        return f'{self.property.house_name} - Apt {self.apartment_no}'
    
    @builtins.property
    def is_available(self):
        """Check if unit is available for rent"""
        from apps.contracts.models import RentalContract
        return not RentalContract.objects.filter(
            unit=self,
            status='active'
        ).exists()


class UnitRoomSummary(models.Model):
    """Room configuration for a unit"""
    
    unit = models.OneToOneField(
        Unit,
        on_delete=models.CASCADE,
        related_name='room_summary',
        primary_key=True
    )
    bedrooms = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    master_bedrooms = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    bathrooms = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    attached_baths = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    common_baths = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    kitchens = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    balconies = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    has_separate_dining = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'unit_room_summary'
        verbose_name_plural = 'Unit Room Summaries'
    
    def __str__(self):
        return f'{self.unit} - {self.bedrooms}BR/{self.bathrooms}BA'


class RentalTerms(models.Model):
    """Rental terms and conditions for a unit"""
    
    unit = models.OneToOneField(
        Unit,
        on_delete=models.CASCADE,
        related_name='rental_terms',
        primary_key=True
    )
    asking_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    minimum_rent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    advance_months = models.IntegerField(
        default=2,
        validators=[MinValueValidator(0)]
    )
    service_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    payment_due_day = models.IntegerField(
        default=5,
        validators=[MinValueValidator(1)],
        help_text='Day of month when rent is due (1-31)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rental_terms'
        verbose_name_plural = 'Rental Terms'
    
    def __str__(self):
        return f'{self.unit} - Rent: {self.asking_rent}'


class UnitPolicy(models.Model):
    """Policies and restrictions for a unit"""
    
    GENDER_CHOICES = [
        ('any', 'Any'),
        ('male', 'Male Only'),
        ('female', 'Female Only'),
    ]
    
    unit = models.OneToOneField(
        Unit,
        on_delete=models.CASCADE,
        related_name='policy',
        primary_key=True
    )
    pets_allowed = models.BooleanField(default=False)
    bachelor_allowed = models.BooleanField(default=True)
    sublet_allowed = models.BooleanField(default=False)
    gender_restricted = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        default='any'
    )
    roof_access = models.BooleanField(default=False)
    roof_gardening_allowed = models.BooleanField(default=False)
    house_gardening_allowed = models.BooleanField(default=False)
    ac_installation_allowed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'unit_policy'
        verbose_name_plural = 'Unit Policies'
    
    def __str__(self):
        return f'{self.unit} - Policy'


class UtilityType(models.Model):
    """Types of utilities"""
    
    name = models.CharField(max_length=50, unique=True)
    
    class Meta:
        db_table = 'utility_types'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class UnitUtility(models.Model):
    """Utility configuration for a unit"""
    
    BILLING_TYPE_CHOICES = [
        ('meter', 'Meter-based'),
        ('card', 'Card/Prepaid'),
        ('fixed', 'Fixed Amount'),
    ]
    
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        related_name='utilities'
    )
    utility_type = models.ForeignKey(
        UtilityType,
        on_delete=models.PROTECT,
        related_name='unit_utilities'
    )
    billing_type = models.CharField(max_length=10, choices=BILLING_TYPE_CHOICES)
    is_included_in_rent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'unit_utility'
        verbose_name_plural = 'Unit Utilities'
        unique_together = [['unit', 'utility_type']]
        indexes = [
            models.Index(fields=['unit', 'utility_type']),
        ]
    
    def __str__(self):
        return f'{self.unit} - {self.utility_type.name}'
