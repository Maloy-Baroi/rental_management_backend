import React from 'react';
import { View, Text, TextInput, TextInputProps } from 'react-native';

interface InputProps extends TextInputProps {
  label?: string;
  error?: string;
  helperText?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

export const Input: React.FC<InputProps> = ({
  label,
  error,
  helperText,
  leftIcon,
  rightIcon,
  className = '',
  ...props
}) => {
  return (
    <View className="mb-4">
      {label && (
        <Text className="text-sm font-semibold text-gray-700 mb-2">{label}</Text>
      )}

      <View
        className={`flex-row items-center bg-white border rounded-lg px-4 ${
          error ? 'border-red-500' : 'border-gray-300'
        } ${className}`}
      >
        {leftIcon && <View className="mr-2">{leftIcon}</View>}

        <TextInput
          className="flex-1 py-3 text-base text-gray-900"
          placeholderTextColor="#9ca3af"
          {...props}
        />

        {rightIcon && <View className="ml-2">{rightIcon}</View>}
      </View>

      {error && (
        <Text className="text-sm text-red-500 mt-1">{error}</Text>
      )}

      {helperText && !error && (
        <Text className="text-sm text-gray-600 mt-1">{helperText}</Text>
      )}
    </View>
  );
};

