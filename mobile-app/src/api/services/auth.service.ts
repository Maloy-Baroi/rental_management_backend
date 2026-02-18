import apiClient, { tokenStorage } from '../client';
import { LoginResponse, RegisterRequest, User } from '@/types';

export const authService = {
  /**
   * Login user
   */
  login: async (phone: string, password: string): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/auth/login/', {
      phone,
      password,
    });

    // Store tokens
    await tokenStorage.setTokens(
      response.data.tokens.access,
      response.data.tokens.refresh
    );

    return response.data;
  },

  /**
   * Register new user
   */
  register: async (data: RegisterRequest): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/auth/register/', data);

    // Store tokens
    await tokenStorage.setTokens(
      response.data.tokens.access,
      response.data.tokens.refresh
    );

    return response.data;
  },

  /**
   * Get current user profile
   */
  getProfile: async (): Promise<User> => {
    const response = await apiClient.get<User>('/auth/profile/');
    return response.data;
  },

  /**
   * Update user profile
   */
  updateProfile: async (data: Partial<User>): Promise<User> => {
    const response = await apiClient.put<User>('/auth/profile/', data);
    return response.data;
  },

  /**
   * Logout user
   */
  logout: async (): Promise<void> => {
    try {
      await apiClient.post('/auth/logout/');
    } catch (error) {
      console.error('Logout API error:', error);
    } finally {
      // Always clear local tokens
      await tokenStorage.clearTokens();
    }
  },

  /**
   * Change password
   */
  changePassword: async (oldPassword: string, newPassword: string): Promise<void> => {
    await apiClient.post('/auth/change-password/', {
      old_password: oldPassword,
      new_password: newPassword,
    });
  },
};

