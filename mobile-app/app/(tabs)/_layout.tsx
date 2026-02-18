import React from 'react';
import { Tabs } from 'expo-router';
import { useAuth } from '@/context/AuthContext';
import { View, Text } from 'react-native';

// Simple icon components (you can replace with react-native-vector-icons later)
const TabIcon = ({ name, focused }: { name: string; focused: boolean }) => (
  <View
    className={`w-8 h-8 rounded-full items-center justify-center ${
      focused ? 'bg-primary-600' : 'bg-gray-300'
    }`}
  >
    <Text className={`text-xs font-bold ${focused ? 'text-white' : 'text-gray-600'}`}>
      {name.substring(0, 1).toUpperCase()}
    </Text>
  </View>
);

export default function TabLayout() {
  const { user } = useAuth();

  if (!user) {
    return null;
  }

  const isOwner = user.role === 'owner';

  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: '#2196f3',
        tabBarInactiveTintColor: '#9ca3af',
        tabBarStyle: {
          backgroundColor: '#ffffff',
          borderTopColor: '#e5e7eb',
          paddingBottom: 8,
          paddingTop: 8,
          height: 60,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '600',
        },
      }}
    >
      <Tabs.Screen
        name="dashboard"
        options={{
          title: 'Dashboard',
          tabBarIcon: ({ focused }) => <TabIcon name="dashboard" focused={focused} />,
        }}
      />

      {isOwner ? (
        <>
          <Tabs.Screen
            name="properties"
            options={{
              title: 'Properties',
              tabBarIcon: ({ focused }) => <TabIcon name="properties" focused={focused} />,
            }}
          />
          <Tabs.Screen
            name="tenants"
            options={{
              title: 'Tenants',
              tabBarIcon: ({ focused }) => <TabIcon name="tenants" focused={focused} />,
            }}
          />
          <Tabs.Screen
            name="billing"
            options={{
              title: 'Billing',
              tabBarIcon: ({ focused }) => <TabIcon name="billing" focused={focused} />,
            }}
          />
        </>
      ) : (
        <>
          <Tabs.Screen
            name="browse"
            options={{
              title: 'Browse',
              tabBarIcon: ({ focused }) => <TabIcon name="browse" focused={focused} />,
            }}
          />
          <Tabs.Screen
            name="payments"
            options={{
              title: 'Payments',
              tabBarIcon: ({ focused }) => <TabIcon name="payments" focused={focused} />,
            }}
          />
        </>
      )}

      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ focused }) => <TabIcon name="profile" focused={focused} />,
        }}
      />

      {/* Hide screens that don't match role */}
      {!isOwner && (
        <>
          <Tabs.Screen name="properties" options={{ href: null }} />
          <Tabs.Screen name="tenants" options={{ href: null }} />
          <Tabs.Screen name="billing" options={{ href: null }} />
        </>
      )}
      {isOwner && (
        <>
          <Tabs.Screen name="browse" options={{ href: null }} />
          <Tabs.Screen name="payments" options={{ href: null }} />
        </>
      )}
    </Tabs>
  );
}

