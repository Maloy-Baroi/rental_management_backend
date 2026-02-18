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
import { UserRole } from '@/types';

export default function RegisterScreen() {
  const { register } = useAuth();
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [role, setRole] = useState<UserRole>('tenant');
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<{
    phone?: string;
    email?: string;
    password?: string;
    confirmPassword?: string;
  }>({});

  const validateForm = (): boolean => {
    const newErrors: any = {};

    if (!phone.trim()) {
      newErrors.phone = 'Phone number is required';
    } else if (!/^\+?[\d\s-]+$/.test(phone)) {
      newErrors.phone = 'Please enter a valid phone number';
    }

    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Please enter a valid email';
    }

    if (!password) {
      newErrors.password = 'Password is required';
    } else if (password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (password !== confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleRegister = async () => {
    if (!validateForm()) return;

    setIsLoading(true);
    try {
      await register(phone, password, email || undefined, role);
      // Navigation is handled in AuthContext after successful registration
    } catch (error: any) {
      console.error('Registration error:', error);

      const errorMessage =
        error?.response?.data?.message ||
        error?.response?.data?.phone?.[0] ||
        error?.response?.data?.email?.[0] ||
        'Registration failed. Please try again.';

      Alert.alert('Registration Failed', errorMessage);
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
        <View className="flex-1 bg-white px-6 py-12">
          {/* Header Section */}
          <View className="items-center mb-8">
            <View className="w-20 h-20 bg-primary-600 rounded-full items-center justify-center mb-4">
              <Text className="text-white text-3xl font-bold">RB</Text>
            </View>
            <Text className="text-3xl font-bold text-gray-900 mb-2">
              Create Account
            </Text>
            <Text className="text-base text-gray-600 text-center">
              Join RentalBridge today
            </Text>
          </View>

          {/* Role Selection */}
          <View className="mb-6">
            <Text className="text-sm font-semibold text-gray-700 mb-3">
              I am a:
            </Text>
            <View className="flex-row gap-3">
              <TouchableOpacity
                className={`flex-1 py-4 rounded-lg border-2 items-center ${
                  role === 'tenant'
                    ? 'bg-primary-50 border-primary-600'
                    : 'bg-white border-gray-300'
                }`}
                onPress={() => setRole('tenant')}
              >
                <Text
                  className={`font-semibold ${
                    role === 'tenant' ? 'text-primary-600' : 'text-gray-600'
                  }`}
                >
                  Tenant
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                className={`flex-1 py-4 rounded-lg border-2 items-center ${
                  role === 'owner'
                    ? 'bg-primary-50 border-primary-600'
                    : 'bg-white border-gray-300'
                }`}
                onPress={() => setRole('owner')}
              >
                <Text
                  className={`font-semibold ${
                    role === 'owner' ? 'text-primary-600' : 'text-gray-600'
                  }`}
                >
                  House Owner
                </Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Form Section */}
          <View className="mb-6">
            <Input
              label="Phone Number *"
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
              label="Email (Optional)"
              placeholder="your@email.com"
              keyboardType="email-address"
              autoCapitalize="none"
              value={email}
              onChangeText={(text) => {
                setEmail(text);
                if (errors.email) setErrors({ ...errors, email: undefined });
              }}
              error={errors.email}
            />

            <Input
              label="Password *"
              placeholder="Min. 6 characters"
              secureTextEntry
              autoCapitalize="none"
              value={password}
              onChangeText={(text) => {
                setPassword(text);
                if (errors.password) setErrors({ ...errors, password: undefined });
              }}
              error={errors.password}
            />

            <Input
              label="Confirm Password *"
              placeholder="Re-enter password"
              secureTextEntry
              autoCapitalize="none"
              value={confirmPassword}
              onChangeText={(text) => {
                setConfirmPassword(text);
                if (errors.confirmPassword)
                  setErrors({ ...errors, confirmPassword: undefined });
              }}
              error={errors.confirmPassword}
            />

            <Button
              title="Create Account"
              onPress={handleRegister}
              isLoading={isLoading}
              fullWidth
              size="lg"
            />
          </View>

          {/* Login Link */}
          <View className="flex-row justify-center items-center mt-4">
            <Text className="text-gray-600 text-base">
              Already have an account?{' '}
            </Text>
            <Link href="/(auth)/login" asChild>
              <TouchableOpacity>
                <Text className="text-primary-600 font-semibold text-base">
                  Sign In
                </Text>
              </TouchableOpacity>
            </Link>
          </View>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

