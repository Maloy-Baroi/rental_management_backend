import apiClient from '../client';
import { Bill, PaginatedResponse } from '@/types';

export const billingService = {
  /**
   * Get all bills
   */
  getBills: async (params?: {
    status?: 'pending' | 'paid' | 'overdue' | 'cancelled';
    page?: number;
  }): Promise<PaginatedResponse<Bill>> => {
    const response = await apiClient.get<PaginatedResponse<Bill>>('/billing/', {
      params,
    });
    return response.data;
  },

  /**
   * Get bill by ID
   */
  getBill: async (id: number): Promise<Bill> => {
    const response = await apiClient.get<Bill>(`/billing/${id}/`);
    return response.data;
  },

  /**
   * Create new bill
   */
  createBill: async (data: Partial<Bill>): Promise<Bill> => {
    const response = await apiClient.post<Bill>('/billing/', data);
    return response.data;
  },

  /**
   * Update bill
   */
  updateBill: async (id: number, data: Partial<Bill>): Promise<Bill> => {
    const response = await apiClient.put<Bill>(`/billing/${id}/`, data);
    return response.data;
  },

  /**
   * Get pending bills
   */
  getPendingBills: async (): Promise<Bill[]> => {
    const response = await apiClient.get<Bill[]>('/billing/pending/');
    return response.data;
  },
};

