from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from apps.contracts.models import RentalContract
from apps.properties.models import UtilityType

User = get_user_model()


class Bill(models.Model):
    """Bills for rent and utilities"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('partial', 'Partially Paid'),
    ]
    
    contract = models.ForeignKey(
        RentalContract,
        on_delete=models.CASCADE,
        related_name='bills'
    )
    utility_type = models.ForeignKey(
        UtilityType,
        on_delete=models.PROTECT,
        related_name='bills',
        null=True,
        blank=True,
        help_text='Null for rent bills'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    billing_month = models.CharField(
        max_length=7,
        db_index=True,
        help_text='Format: YYYY-MM'
    )
    due_date = models.DateField(db_index=True)
    paid_on = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    external_ref = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='External reference (e.g., utility bill number)'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'bills'
        ordering = ['-billing_month', '-due_date']
        indexes = [
            models.Index(fields=['contract', 'billing_month']),
            models.Index(fields=['contract', 'status']),
            models.Index(fields=['due_date', 'status']),
        ]
        unique_together = [['contract', 'billing_month', 'utility_type']]
    
    def __str__(self):
        bill_type = self.utility_type.name if self.utility_type else 'Rent'
        return f'{self.contract} - {bill_type} ({self.billing_month})'
    
    @property
    def is_overdue(self):
        """Check if bill is overdue"""
        from django.utils import timezone
        return self.status == 'pending' and self.due_date < timezone.now().date()
    
    @property
    def amount_paid(self):
        """Calculate total amount paid"""
        return self.payments.filter(
            status='succeeded'
        ).aggregate(
            total=models.Sum('amount')
        )['total'] or 0
    
    @property
    def amount_remaining(self):
        """Calculate remaining amount"""
        return self.amount - self.amount_paid
