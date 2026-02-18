from rest_framework import serializers
from .models import RentalContract, RentalContractParticipant
from apps.properties.serializers import UnitSerializer
from apps.accounts.models import Household


class RentalContractSerializer(serializers.ModelSerializer):
    """Serializer for RentalContract model"""

    unit_detail = UnitSerializer(source='unit', read_only=True)
    tenant_household_name = serializers.CharField(source='tenant_household.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    duration_days = serializers.SerializerMethodField()

    class Meta:
        model = RentalContract
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def get_duration_days(self, obj):
        """Calculate contract duration in days"""
        return (obj.contract_to - obj.contract_from).days

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class RentalContractParticipantSerializer(serializers.ModelSerializer):
    """Serializer for RentalContractParticipant model"""

    contract_detail = RentalContractSerializer(source='contract', read_only=True)
    household_member_name = serializers.CharField(source='household_member.get_full_name', read_only=True)

    class Meta:
        model = RentalContractParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

