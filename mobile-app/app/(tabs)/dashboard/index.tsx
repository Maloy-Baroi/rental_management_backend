import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { useAuth } from '@/context/AuthContext';
import { Card, CardHeader, CardContent } from '@/components/ui/Card';
import { DashboardCardSkeleton } from '@/components/ui/LoadingSkeleton';
import { dashboardService } from '@/api/services/dashboard.service';
import { OwnerDashboardStats, TenantDashboardStats } from '@/types';

export default function DashboardScreen() {
  const { user } = useAuth();
  const [ownerStats, setOwnerStats] = useState<OwnerDashboardStats | null>(null);
  const [tenantStats, setTenantStats] = useState<TenantDashboardStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const isOwner = user?.role === 'owner';

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      if (isOwner) {
        const data = await dashboardService.getOwnerStats();
        setOwnerStats(data);
      } else {
        const data = await dashboardService.getTenantStats();
        setTenantStats(data);
      }
    } catch (error: any) {
      console.error('Dashboard error:', error);
      Alert.alert(
        'Error',
        error?.response?.data?.message || 'Failed to load dashboard data'
      );
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadDashboard();
  };

  const formatCurrency = (amount: number) => {
    return `৳${amount.toLocaleString()}`;
  };

  if (isLoading) {
    return (
      <View className="flex-1 bg-gray-50">
        <View className="bg-primary-600 pt-12 pb-6 px-6">
          <Text className="text-white text-2xl font-bold">Dashboard</Text>
        </View>
        <ScrollView className="flex-1 px-6 pt-6">
          <DashboardCardSkeleton />
          <DashboardCardSkeleton />
          <DashboardCardSkeleton />
        </ScrollView>
      </View>
    );
  }

  return (
    <View className="flex-1 bg-gray-50">
      {/* Header */}
      <View className="bg-primary-600 pt-12 pb-6 px-6">
        <Text className="text-white text-2xl font-bold">Dashboard</Text>
        <Text className="text-white/80 text-sm mt-1">
          Welcome back, {user?.phone}
        </Text>
      </View>

      <ScrollView
        className="flex-1 px-6 pt-6"
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {isOwner && ownerStats ? (
          // Owner Dashboard
          <>
            {/* Pending Rent Card */}
            <Card variant="elevated" className="mb-4">
              <CardHeader
                title="Pending Rent"
                subtitle={`${ownerStats.pending_rent_count} pending bills`}
                rightElement={
                  <View className="w-12 h-12 bg-accent-100 rounded-full items-center justify-center">
                    <Text className="text-accent-600 text-xl font-bold">৳</Text>
                  </View>
                }
              />
              <CardContent>
                <Text className="text-3xl font-bold text-gray-900">
                  {formatCurrency(ownerStats.pending_rent_amount)}
                </Text>
                <TouchableOpacity className="mt-4 bg-primary-600 py-2 px-4 rounded-lg">
                  <Text className="text-white font-semibold text-center">
                    View Details
                  </Text>
                </TouchableOpacity>
              </CardContent>
            </Card>

            {/* Properties Overview */}
            <Card variant="elevated" className="mb-4">
              <CardHeader
                title="Properties"
                subtitle="Your property portfolio"
                rightElement={
                  <View className="w-12 h-12 bg-primary-100 rounded-full items-center justify-center">
                    <Text className="text-primary-600 text-xl font-bold">🏠</Text>
                  </View>
                }
              />
              <CardContent>
                <View className="flex-row justify-between mb-4">
                  <View>
                    <Text className="text-2xl font-bold text-gray-900">
                      {ownerStats.total_properties}
                    </Text>
                    <Text className="text-sm text-gray-600">Total Buildings</Text>
                  </View>
                  <View>
                    <Text className="text-2xl font-bold text-gray-900">
                      {ownerStats.total_units}
                    </Text>
                    <Text className="text-sm text-gray-600">Total Units</Text>
                  </View>
                </View>

                <View className="flex-row justify-between">
                  <View className="flex-1 mr-2 bg-secondary-50 p-3 rounded-lg">
                    <Text className="text-lg font-bold text-secondary-700">
                      {ownerStats.occupied_units}
                    </Text>
                    <Text className="text-xs text-gray-600">Occupied</Text>
                  </View>
                  <View className="flex-1 ml-2 bg-gray-100 p-3 rounded-lg">
                    <Text className="text-lg font-bold text-gray-700">
                      {ownerStats.vacant_units}
                    </Text>
                    <Text className="text-xs text-gray-600">Vacant</Text>
                  </View>
                </View>
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <Card variant="elevated" className="mb-4">
              <CardHeader title="Quick Actions" />
              <CardContent>
                <View className="flex-row flex-wrap gap-3">
                  <TouchableOpacity className="flex-1 min-w-[45%] bg-primary-600 py-4 rounded-lg items-center">
                    <Text className="text-white font-semibold">Add Property</Text>
                  </TouchableOpacity>
                  <TouchableOpacity className="flex-1 min-w-[45%] bg-secondary-600 py-4 rounded-lg items-center">
                    <Text className="text-white font-semibold">Post Rent</Text>
                  </TouchableOpacity>
                  <TouchableOpacity className="flex-1 min-w-[45%] bg-accent-600 py-4 rounded-lg items-center">
                    <Text className="text-white font-semibold">Generate Bill</Text>
                  </TouchableOpacity>
                  <TouchableOpacity className="flex-1 min-w-[45%] bg-gray-600 py-4 rounded-lg items-center">
                    <Text className="text-white font-semibold">View Tenants</Text>
                  </TouchableOpacity>
                </View>
              </CardContent>
            </Card>

            {/* Tenants */}
            <Card variant="elevated" className="mb-6">
              <CardHeader
                title="Tenants"
                rightElement={
                  <View className="w-12 h-12 bg-secondary-100 rounded-full items-center justify-center">
                    <Text className="text-secondary-600 text-xl font-bold">👥</Text>
                  </View>
                }
              />
              <CardContent>
                <Text className="text-3xl font-bold text-gray-900">
                  {ownerStats.total_tenants}
                </Text>
                <Text className="text-sm text-gray-600 mt-1">Active tenants</Text>
              </CardContent>
            </Card>
          </>
        ) : (
          // Tenant Dashboard
          tenantStats && (
            <>
              {/* Next Payment Card */}
              {tenantStats.next_payment && (
                <Card variant="elevated" className="mb-4">
                  <CardHeader
                    title="Next Payment Due"
                    subtitle={`Due in ${tenantStats.next_payment.days_remaining} days`}
                    rightElement={
                      <View className="w-12 h-12 bg-accent-100 rounded-full items-center justify-center">
                        <Text className="text-accent-600 text-xl font-bold">💰</Text>
                      </View>
                    }
                  />
                  <CardContent>
                    <Text className="text-3xl font-bold text-gray-900 mb-2">
                      {formatCurrency(tenantStats.next_payment.amount)}
                    </Text>
                    <Text className="text-sm text-gray-600 mb-4">
                      Due Date:{' '}
                      {new Date(tenantStats.next_payment.due_date).toLocaleDateString()}
                    </Text>
                    <TouchableOpacity className="bg-primary-600 py-3 px-4 rounded-lg">
                      <Text className="text-white font-semibold text-center">
                        Pay Now
                      </Text>
                    </TouchableOpacity>
                  </CardContent>
                </Card>
              )}

              {/* Current Rental */}
              {tenantStats.current_contract && (
                <Card variant="elevated" className="mb-4">
                  <CardHeader
                    title="My Current Rental"
                    rightElement={
                      <View className="w-12 h-12 bg-primary-100 rounded-full items-center justify-center">
                        <Text className="text-primary-600 text-xl font-bold">🏠</Text>
                      </View>
                    }
                  />
                  <CardContent>
                    <View className="mb-3">
                      <Text className="text-sm text-gray-600">Monthly Rent</Text>
                      <Text className="text-2xl font-bold text-gray-900">
                        {formatCurrency(tenantStats.current_contract.rent_amount)}
                      </Text>
                    </View>
                    <View className="flex-row justify-between">
                      <View>
                        <Text className="text-xs text-gray-600">Start Date</Text>
                        <Text className="text-sm font-semibold text-gray-900">
                          {new Date(
                            tenantStats.current_contract.start_date
                          ).toLocaleDateString()}
                        </Text>
                      </View>
                      <View>
                        <Text className="text-xs text-gray-600">End Date</Text>
                        <Text className="text-sm font-semibold text-gray-900">
                          {new Date(
                            tenantStats.current_contract.end_date
                          ).toLocaleDateString()}
                        </Text>
                      </View>
                    </View>
                  </CardContent>
                </Card>
              )}

              {/* Payment History Summary */}
              <Card variant="elevated" className="mb-4">
                <CardHeader
                  title="Payment History"
                  rightElement={
                    <View className="w-12 h-12 bg-secondary-100 rounded-full items-center justify-center">
                      <Text className="text-secondary-600 text-xl font-bold">📊</Text>
                    </View>
                  }
                />
                <CardContent>
                  <View className="mb-3">
                    <Text className="text-sm text-gray-600">Total Paid</Text>
                    <Text className="text-2xl font-bold text-secondary-600">
                      {formatCurrency(tenantStats.total_paid)}
                    </Text>
                  </View>
                  {tenantStats.last_payment && (
                    <View className="mt-3 pt-3 border-t border-gray-200">
                      <Text className="text-xs text-gray-600 mb-1">Last Payment</Text>
                      <View className="flex-row justify-between items-center">
                        <Text className="text-sm font-semibold text-gray-900">
                          {formatCurrency(tenantStats.last_payment.amount)}
                        </Text>
                        <Text className="text-xs text-gray-600">
                          {new Date(
                            tenantStats.last_payment.payment_date
                          ).toLocaleDateString()}
                        </Text>
                      </View>
                    </View>
                  )}
                </CardContent>
              </Card>

              {/* Browse Properties */}
              <Card variant="elevated" className="mb-6">
                <CardHeader title="Looking for a New Place?" />
                <CardContent>
                  <TouchableOpacity className="bg-primary-600 py-3 px-4 rounded-lg">
                    <Text className="text-white font-semibold text-center">
                      Browse Available Properties
                    </Text>
                  </TouchableOpacity>
                </CardContent>
              </Card>
            </>
          )
        )}
      </ScrollView>
    </View>
  );
}

