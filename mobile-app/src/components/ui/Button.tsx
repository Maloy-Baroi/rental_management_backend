import React from 'react';
import { TouchableOpacity, Text, ActivityIndicator, TouchableOpacityProps } from 'react-native';

interface ButtonProps extends TouchableOpacityProps {
  title: string;
  variant?: 'primary' | 'secondary' | 'outline' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  fullWidth?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  title,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  fullWidth = false,
  disabled,
  className = '',
  ...props
}) => {
  const variantStyles = {
    primary: 'bg-primary-600 active:bg-primary-700',
    secondary: 'bg-secondary-600 active:bg-secondary-700',
    outline: 'bg-transparent border-2 border-primary-600 active:bg-primary-50',
    danger: 'bg-red-600 active:bg-red-700',
  };

  const sizeStyles = {
    sm: 'px-4 py-2',
    md: 'px-6 py-3',
    lg: 'px-8 py-4',
  };

  const textSizeStyles = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
  };

  const textColorStyles = {
    primary: 'text-white',
    secondary: 'text-white',
    outline: 'text-primary-600',
    danger: 'text-white',
  };

  const disabledStyle = disabled || isLoading ? 'opacity-50' : '';
  const widthStyle = fullWidth ? 'w-full' : '';

  return (
    <TouchableOpacity
      className={`rounded-lg items-center justify-center ${variantStyles[variant]} ${sizeStyles[size]} ${disabledStyle} ${widthStyle} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <ActivityIndicator color={variant === 'outline' ? '#2196f3' : '#ffffff'} />
      ) : (
        <Text className={`font-semibold ${textSizeStyles[size]} ${textColorStyles[variant]}`}>
          {title}
        </Text>
      )}
    </TouchableOpacity>
  );
};

