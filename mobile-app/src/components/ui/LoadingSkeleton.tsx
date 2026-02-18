import React from 'react';
import { View } from 'react-native';

interface SkeletonProps {
  width?: string;
  height?: string;
  rounded?: boolean;
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({
  width = 'w-full',
  height = 'h-4',
  rounded = false,
  className = '',
}) => {
  return (
    <View
      className={`bg-gray-200 animate-pulse ${width} ${height} ${
        rounded ? 'rounded-full' : 'rounded'
      } ${className}`}
    />
  );
};

export const CardSkeleton: React.FC = () => {
  return (
    <View className="bg-white rounded-xl p-4 mb-4">
      <Skeleton width="w-3/4" height="h-6" className="mb-2" />
      <Skeleton width="w-1/2" height="h-4" className="mb-4" />
      <Skeleton width="w-full" height="h-20" />
    </View>
  );
};

export const DashboardCardSkeleton: React.FC = () => {
  return (
    <View className="bg-white rounded-xl p-6 mb-4 shadow-sm">
      <View className="flex-row items-center justify-between mb-4">
        <Skeleton width="w-1/3" height="h-5" />
        <Skeleton width="w-10" height="h-10" rounded />
      </View>
      <Skeleton width="w-1/2" height="h-8" className="mb-2" />
      <Skeleton width="w-2/3" height="h-4" />
    </View>
  );
};

