from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class AuditLog(models.Model):
    """Audit trail for all critical operations"""
    
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('terminate', 'Terminate'),
        ('renew', 'Renew'),
        ('payment', 'Payment'),
        ('refund', 'Refund'),
    ]
    
    # Generic relation to any model
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    object_id = models.BigIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    # Legacy fields for backward compatibility
    entity_type = models.CharField(
        max_length=100,
        db_index=True,
        help_text='Type of entity (e.g., RentalContract, Payment)'
    )
    entity_id = models.BigIntegerField(
        db_index=True,
        help_text='ID of the entity'
    )
    
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        db_index=True
    )
    data = models.JSONField(
        default=dict,
        help_text='Snapshot of changed data'
    )
    actor_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        help_text='User who performed the action'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'audit_logs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['entity_type', 'entity_id']),
            models.Index(fields=['action', 'created_at']),
            models.Index(fields=['actor_user', 'created_at']),
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def __str__(self):
        actor = self.actor_user.phone if self.actor_user else 'System'
        return f'{actor} - {self.action} - {self.entity_type}:{self.entity_id}'
    
    @classmethod
    def log(cls, entity_type, entity_id, action, data, user=None, request=None, content_object=None):
        """
        Create an audit log entry
        
        Args:
            entity_type: Type of entity
            entity_id: ID of entity
            action: Action performed
            data: Data snapshot
            user: User who performed action
            request: HTTP request object
            content_object: Django model instance (optional)
        """
        log_data = {
            'entity_type': entity_type,
            'entity_id': entity_id,
            'action': action,
            'data': data,
            'actor_user': user,
        }
        
        if content_object:
            log_data['content_object'] = content_object
        
        if request:
            log_data['ip_address'] = cls._get_client_ip(request)
            log_data['user_agent'] = request.META.get('HTTP_USER_AGENT', '')
        
        return cls.objects.create(**log_data)
    
    @staticmethod
    def _get_client_ip(request):
        """Extract client IP from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
