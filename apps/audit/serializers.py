from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for AuditLog model"""

    actor_name = serializers.CharField(source='actor_user.get_full_name', read_only=True)
    actor_phone = serializers.CharField(source='actor_user.phone', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id',
            'entity_type',
            'entity_id',
            'content_type',
            'content_type_name',
            'object_id',
            'action',
            'action_display',
            'data',
            'actor_user',
            'actor_name',
            'actor_phone',
            'ip_address',
            'user_agent',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

