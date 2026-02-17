from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from apps.properties.models import Unit
from apps.accounts.models import Household

User = get_user_model()


class RentalContract(models.Model):
    """Rental contract between landlord and tenant"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('terminated', 'Terminated'),
        ('expired', 'Expired'),
    ]
    
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name='rental_contracts'
    )
    tenant_household = models.ForeignKey(
        Household,
        on_delete=models.PROTECT,
        related_name='rental_contracts'
    )
    contract_from = models.DateField(db_index=True)
    contract_to = models.DateField(db_index=True)
    rent_amount_at_contract = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    advance_paid_months = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    service_charge_at_contract = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)]
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active',
        db_index=True
    )
    terminated_at = models.DateTimeField(null=True, blank=True)
    termination_reason = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='contracts_created'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'rental_contracts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['unit', 'status']),
            models.Index(fields=['tenant_household', 'status']),
            models.Index(fields=['contract_from', 'contract_to']),
        ]
    
    def __str__(self):
        return f'{self.unit} - {self.tenant_household.name} ({self.status})'
    
    def clean(self):
        # Validate contract dates
        if self.contract_to <= self.contract_from:
            raise ValidationError('Contract end date must be after start date')
        
        # Check for overlapping active contracts
        if self.status == 'active':
            overlapping = RentalContract.objects.filter(
                unit=self.unit,
                status='active'
            ).exclude(pk=self.pk)
            
            if overlapping.exists():
                raise ValidationError('Unit already has an active rental contract')
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class RentalContractParticipant(models.Model):
    """Additional participants in a rental contract"""
    
    ROLE_CHOICES = [
        ('primary', 'Primary Tenant'),
        ('dependent', 'Dependent'),
    ]
    
    contract = models.ForeignKey(
        RentalContract,
        on_delete=models.CASCADE,
        related_name='participants'
    )
    household = models.ForeignKey(
        Household,
        on_delete=models.PROTECT,
        related_name='contract_participations'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rental_contract_participants'
        unique_together = [['contract', 'household']]
        indexes = [
            models.Index(fields=['contract', 'role']),
        ]
    
    def __str__(self):
        return f'{self.contract} - {self.household.name} ({self.role})'


class RentalContractAuthor(models.Model):
    """Authorized users who can manage a rental contract"""
    
    ROLE_CHOICES = [
        ('primary', 'Primary Author'),
        ('co-author', 'Co-Author'),
    ]
    
    contract = models.ForeignKey(
        RentalContract,
        on_delete=models.CASCADE,
        related_name='authors'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contract_authorships'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    can_approve = models.BooleanField(default=False)
    can_terminate = models.BooleanField(default=False)
    can_renew = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'rental_contract_authors'
        unique_together = [['contract', 'user']]
        indexes = [
            models.Index(fields=['contract', 'is_active']),
            models.Index(fields=['user', 'is_active']),
        ]
    
    def __str__(self):
        return f'{self.contract} - {self.user.phone} ({self.role})'
