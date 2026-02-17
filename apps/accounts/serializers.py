from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import Household

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'password', 'password_confirm']
        read_only_fields = ['id']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({'password': 'Password fields do not match'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user details"""
    
    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class HouseholdSerializer(serializers.ModelSerializer):
    """Serializer for household"""
    
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Household
        fields = [
            'id', 'user', 'name', 'date_of_birth', 'nid',
            'contact_phone', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class HouseholdCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating household"""
    
    class Meta:
        model = Household
        fields = ['name', 'date_of_birth', 'nid', 'contact_phone']
    
    def create(self, validated_data):
        user = self.context['request'].user
        return Household.objects.create(user=user, **validated_data)


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change"""
    
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({'new_password': 'Password fields do not match'})
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value
