import apiClient from '../client';
import { Payment, PaginatedResponse } from '@/types';

export const paymentService = {
  /**
   * Get all payments
   */
  getPayments: async (params?: {
    page?: number;
  }): Promise<PaginatedResponse<Payment>> => {
    const response = await apiClient.get<PaginatedResponse<Payment>>('/payments/', {
      params,
    });
    return response.data;
  },

  /**
   * Get payment by ID
   */
  getPayment: async (id: number): Promise<Payment> => {
    const response = await apiClient.get<Payment>(`/payments/${id}/`);
    return response.data;
  },

  /**
   * Make payment
   */
  makePayment: async (data: {
    bill: number;
    amount: number;
    payment_method: 'bkash' | 'nagad' | 'rocket' | 'bank_transfer' | 'cash';
    transaction_id?: string;
  }): Promise<Payment> => {
    const response = await apiClient.post<Payment>('/payments/', data);
    return response.data;
  },

  /**
   * Download payment receipt
   */
  downloadReceipt: async (id: number): Promise<Blob> => {
    const response = await apiClient.get(`/payments/receipt/${id}/`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

