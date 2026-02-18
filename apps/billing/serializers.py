from rest_framework import serializers
from .models import Bill
from apps.contracts.serializers import RentalContractSerializer
from apps.properties.serializers import UtilityTypeSerializer


class BillSerializer(serializers.ModelSerializer):
    """Serializer for Bill model"""

    contract_detail = RentalContractSerializer(source='contract', read_only=True)
    utility_type_detail = UtilityTypeSerializer(source='utility_type', read_only=True)
    amount_paid = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    amount_remaining = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    bill_type = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'paid_on')

    def get_bill_type(self, obj):
        """Get human-readable bill type"""
        return obj.utility_type.name if obj.utility_type else 'Rent'

