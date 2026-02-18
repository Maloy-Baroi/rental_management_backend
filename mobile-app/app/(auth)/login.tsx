import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  KeyboardAvoidingView,
  Platform,
  Alert,
  TouchableOpacity,
} from 'react-native';
import { Link } from 'expo-router';
import { useAuth } from '@/context/AuthContext';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';

export default function LoginScreen() {
  const { login } = useAuth();
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<{ phone?: string; password?: string }>({});

  const validateForm = (): boolean => {
    const newErrors: { phone?: string; password?: string } = {};

    if (!phone.trim()) {
      newErrors.phone = 'Phone number is required';
    } else if (!/^\+?[\d\s-]+$/.test(phone)) {
      newErrors.phone = 'Please enter a valid phone number';
    }

    if (!password) {
      newErrors.password = 'Password is required';
    } else if (password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleLogin = async () => {
    if (!validateForm()) return;

    setIsLoading(true);
    try {
      await login(phone, password);
      // Navigation is handled in AuthContext after successful login
    } catch (error: any) {
      console.error('Login error:', error);

      const errorMessage =
        error?.response?.data?.message ||
        error?.response?.data?.detail ||
        'Login failed. Please check your credentials.';

      Alert.alert('Login Failed', errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      className="flex-1"
    >
      <ScrollView
        contentContainerClassName="flex-grow"
        keyboardShouldPersistTaps="handled"
      >
        <View className="flex-1 bg-white px-6 justify-center">
          {/* Logo/Header Section */}
          <View className="items-center mb-12">
            <View className="w-20 h-20 bg-primary-600 rounded-full items-center justify-center mb-4">
              <Text className="text-white text-3xl font-bold">RB</Text>
            </View>
            <Text className="text-3xl font-bold text-gray-900 mb-2">
              Welcome Back
            </Text>
            <Text className="text-base text-gray-600 text-center">
              Sign in to continue to RentalBridge
            </Text>
          </View>

          {/* Form Section */}
          <View className="mb-6">
            <Input
              label="Phone Number"
              placeholder="+880 1XXX-XXXXXX"
              keyboardType="phone-pad"
              autoCapitalize="none"
              value={phone}
              onChangeText={(text) => {
                setPhone(text);
                if (errors.phone) setErrors({ ...errors, phone: undefined });
              }}
              error={errors.phone}
            />

            <Input
              label="Password"
              placeholder="Enter your password"
              secureTextEntry
              autoCapitalize="none"
              value={password}
              onChangeText={(text) => {
                setPassword(text);
                if (errors.password) setErrors({ ...errors, password: undefined });
              }}
              error={errors.password}
            />

            <TouchableOpacity className="items-end mb-6">
              <Text className="text-primary-600 font-semibold">
                Forgot Password?
              </Text>
            </TouchableOpacity>

            <Button
              title="Sign In"
              onPress={handleLogin}
              isLoading={isLoading}
              fullWidth
              size="lg"
            />
          </View>

          {/* Register Link */}
          <View className="flex-row justify-center items-center mt-6">
            <Text className="text-gray-600 text-base">
              Don't have an account?{' '}
            </Text>
            <Link href="/(auth)/register" asChild>
              <TouchableOpacity>
                <Text className="text-primary-600 font-semibold text-base">
                  Sign Up
                </Text>
              </TouchableOpacity>
            </Link>
          </View>

          {/* Development Helper */}
          {__DEV__ && (
            <View className="mt-8 p-4 bg-gray-100 rounded-lg">
              <Text className="text-xs text-gray-600 text-center">
                Development Mode: Test credentials will be shown here
              </Text>
            </View>
          )}
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

