from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from apps.contracts.models import RentalContract
from apps.billing.models import Bill

User = get_user_model()


class Payment(models.Model):
    """Payment transactions"""
    
    PAYMENT_TYPE_CHOICES = [
        ('rent', 'Rent Payment'),
        ('utility', 'Utility Payment'),
        ('service', 'Service Charge'),
        ('advance', 'Advance Payment'),
    ]
    
    PROVIDER_CHOICES = [
        ('stripe', 'Stripe'),
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeeded'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    contract = models.ForeignKey(
        RentalContract,
        on_delete=models.PROTECT,
        related_name='payments'
    )
    bill = models.ForeignKey(
        Bill,
        on_delete=models.SET_NULL,
        related_name='payments',
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_TYPE_CHOICES,
        db_index=True
    )
    provider = models.CharField(
        max_length=50,
        choices=PROVIDER_CHOICES,
        default='stripe'
    )
    provider_payment_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        help_text='Payment ID from payment provider'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    idempotency_key = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text='Unique key to prevent duplicate payments'
    )
    received_by_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments_received',
        help_text='User who received the payment (for cash/manual)'
    )
    metadata = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional payment metadata'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['contract', 'status']),
            models.Index(fields=['bill', 'status']),
            models.Index(fields=['provider', 'provider_payment_id']),
            models.Index(fields=['created_at', 'status']),
        ]
    
    def __str__(self):
        return f'{self.contract} - {self.payment_type} - {self.amount} ({self.status})'


class PaymentWebhook(models.Model):
    """Store webhook events from payment providers"""
    
    provider = models.CharField(max_length=50)
    event_id = models.CharField(max_length=255, unique=True, db_index=True)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    processed = models.BooleanField(default=False, db_index=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'payment_webhooks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['provider', 'processed']),
            models.Index(fields=['event_type', 'processed']),
        ]
    
    def __str__(self):
        return f'{self.provider} - {self.event_type} ({self.event_id})'
