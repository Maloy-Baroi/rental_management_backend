from rest_framework import serializers
from .models import Payment
from apps.contracts.serializers import RentalContractSerializer
from apps.billing.serializers import BillSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""

    contract_detail = RentalContractSerializer(source='contract', read_only=True)
    bill_detail = BillSerializer(source='bill', read_only=True)
    received_by_name = serializers.CharField(source='received_by_user.get_full_name', read_only=True)
    payment_type_display = serializers.CharField(source='get_payment_type_display', read_only=True)
    provider_display = serializers.CharField(source='get_provider_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

