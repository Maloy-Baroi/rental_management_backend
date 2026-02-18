from rest_framework import serializers
from .models import Location, Property, Unit, UtilityType


class LocationSerializer(serializers.ModelSerializer):
    """Serializer for Location model"""

    class Meta:
        model = Location
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class PropertySerializer(serializers.ModelSerializer):
    """Serializer for Property model"""

    location_detail = LocationSerializer(source='location', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    total_units = serializers.IntegerField(source='units.count', read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class UnitSerializer(serializers.ModelSerializer):
    """Serializer for Unit model"""

    property_detail = PropertySerializer(source='property', read_only=True)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class UtilityTypeSerializer(serializers.ModelSerializer):
    """Serializer for UtilityType model"""

    class Meta:
        model = UtilityType
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

