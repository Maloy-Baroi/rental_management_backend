import apiClient from '../client';
import { OwnerDashboardStats, TenantDashboardStats } from '@/types';

export const dashboardService = {
  /**
   * Get owner dashboard statistics
   */
  getOwnerStats: async (): Promise<OwnerDashboardStats> => {
    const response = await apiClient.get<OwnerDashboardStats>('/properties/dashboard-stats/');
    return response.data;
  },

  /**
   * Get tenant dashboard statistics
   */
  getTenantStats: async (): Promise<TenantDashboardStats> => {
    const response = await apiClient.get<TenantDashboardStats>('/properties/dashboard-stats/');
    return response.data;
  },
};

