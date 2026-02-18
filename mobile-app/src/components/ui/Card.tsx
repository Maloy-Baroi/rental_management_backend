import React, { ReactNode } from 'react';
import { View, Text, ViewProps } from 'react-native';

interface CardProps extends ViewProps {
  children: ReactNode;
  variant?: 'default' | 'elevated' | 'outlined';
}

export const Card: React.FC<CardProps> = ({
  children,
  variant = 'default',
  className = '',
  ...props
}) => {
  const variantStyles = {
    default: 'bg-white',
    elevated: 'bg-white shadow-lg shadow-gray-300',
    outlined: 'bg-white border border-gray-200',
  };

  return (
    <View
      className={`rounded-xl p-4 ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {children}
    </View>
  );
};

interface CardHeaderProps {
  title: string;
  subtitle?: string;
  rightElement?: ReactNode;
}

export const CardHeader: React.FC<CardHeaderProps> = ({
  title,
  subtitle,
  rightElement,
}) => {
  return (
    <View className="flex-row items-center justify-between mb-3">
      <View className="flex-1">
        <Text className="text-lg font-bold text-gray-900">{title}</Text>
        {subtitle && (
          <Text className="text-sm text-gray-600 mt-1">{subtitle}</Text>
        )}
      </View>
      {rightElement && <View>{rightElement}</View>}
    </View>
  );
};

interface CardContentProps {
  children: ReactNode;
}

export const CardContent: React.FC<CardContentProps> = ({ children }) => {
  return <View>{children}</View>;
};

