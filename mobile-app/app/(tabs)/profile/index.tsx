import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { useAuth } from '@/context/AuthContext';
import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';

export default function ProfileScreen() {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Logout',
        style: 'destructive',
        onPress: async () => {
          await logout();
        },
      },
    ]);
  };

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case 'owner':
        return 'bg-primary-100 text-primary-700';
      case 'tenant':
        return 'bg-secondary-100 text-secondary-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <View className="flex-1 bg-gray-50">
      {/* Header */}
      <View className="bg-primary-600 pt-12 pb-20 px-6">
        <Text className="text-white text-2xl font-bold">Profile</Text>
      </View>

      <ScrollView className="flex-1 px-6" style={{ marginTop: -40 }}>
        {/* Profile Card */}
        <Card variant="elevated" className="mb-4">
          <CardContent>
            <View className="items-center py-4">
              <View className="w-24 h-24 bg-primary-600 rounded-full items-center justify-center mb-4">
                <Text className="text-white text-3xl font-bold">
                  {user?.phone.substring(0, 2).toUpperCase()}
                </Text>
              </View>
              
              <Text className="text-xl font-bold text-gray-900">{user?.phone}</Text>
              
              {user?.email && (
                <Text className="text-sm text-gray-600 mt-1">{user.email}</Text>
              )}
              
              <View className={`mt-3 px-4 py-2 rounded-full ${getRoleBadgeColor(user?.role || '')}`}>
                <Text className="text-sm font-semibold capitalize">
                  {user?.role}
                </Text>
              </View>
            </View>
          </CardContent>
        </Card>

        {/* Account Information */}
        <Card variant="elevated" className="mb-4">
          <CardContent>
            <Text className="text-lg font-bold text-gray-900 mb-4">
              Account Information
            </Text>
            
            <View className="space-y-3">
              <View className="flex-row justify-between py-3 border-b border-gray-100">
                <Text className="text-gray-600">Phone Number</Text>
                <Text className="font-semibold text-gray-900">{user?.phone}</Text>
              </View>
              
              <View className="flex-row justify-between py-3 border-b border-gray-100">
                <Text className="text-gray-600">Email</Text>
                <Text className="font-semibold text-gray-900">
                  {user?.email || 'Not set'}
                </Text>
              </View>
              
              <View className="flex-row justify-between py-3 border-b border-gray-100">
                <Text className="text-gray-600">Account Type</Text>
                <Text className="font-semibold text-gray-900 capitalize">
                  {user?.role}
                </Text>
              </View>
              
              <View className="flex-row justify-between py-3">
                <Text className="text-gray-600">Member Since</Text>
                <Text className="font-semibold text-gray-900">
                  {user?.created_at
                    ? new Date(user.created_at).toLocaleDateString()
                    : 'N/A'}
                </Text>
              </View>
            </View>
          </CardContent>
        </Card>

        {/* Actions */}
        <Card variant="elevated" className="mb-4">
          <CardContent>
            <Text className="text-lg font-bold text-gray-900 mb-4">Settings</Text>
            
            <TouchableOpacity className="flex-row justify-between items-center py-3 border-b border-gray-100">
              <Text className="text-gray-900">Edit Profile</Text>
              <Text className="text-gray-400">›</Text>
            </TouchableOpacity>
            
            <TouchableOpacity className="flex-row justify-between items-center py-3 border-b border-gray-100">
              <Text className="text-gray-900">Change Password</Text>
              <Text className="text-gray-400">›</Text>
            </TouchableOpacity>
            
            <TouchableOpacity className="flex-row justify-between items-center py-3 border-b border-gray-100">
              <Text className="text-gray-900">Notifications</Text>
              <Text className="text-gray-400">›</Text>
            </TouchableOpacity>
            
            <TouchableOpacity className="flex-row justify-between items-center py-3">
              <Text className="text-gray-900">Privacy & Security</Text>
              <Text className="text-gray-400">›</Text>
            </TouchableOpacity>
          </CardContent>
        </Card>

        {/* Logout Button */}
        <View className="mb-8">
          <Button
            title="Logout"
            variant="danger"
            onPress={handleLogout}
            fullWidth
            size="lg"
          />
        </View>

        {/* App Version */}
        <Text className="text-center text-gray-500 text-sm mb-6">
          RentalBridge v1.0.0
        </Text>
      </ScrollView>
    </View>
  );
}

