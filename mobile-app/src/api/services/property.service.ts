import apiClient from '../client';
import { Property, Unit, PaginatedResponse } from '@/types';

export const propertyService = {
  /**
   * Get all properties
   */
  getProperties: async (params?: {
    page?: number;
    search?: string;
  }): Promise<PaginatedResponse<Property>> => {
    const response = await apiClient.get<PaginatedResponse<Property>>('/properties/', {
      params,
    });
    return response.data;
  },

  /**
   * Get property by ID
   */
  getProperty: async (id: number): Promise<Property> => {
    const response = await apiClient.get<Property>(`/properties/${id}/`);
    return response.data;
  },

  /**
   * Create new property
   */
  createProperty: async (data: Partial<Property>): Promise<Property> => {
    const response = await apiClient.post<Property>('/properties/', data);
    return response.data;
  },

  /**
   * Update property
   */
  updateProperty: async (id: number, data: Partial<Property>): Promise<Property> => {
    const response = await apiClient.put<Property>(`/properties/${id}/`, data);
    return response.data;
  },

  /**
   * Delete property
   */
  deleteProperty: async (id: number): Promise<void> => {
    await apiClient.delete(`/properties/${id}/`);
  },

  /**
   * Get all units
   */
  getUnits: async (params?: {
    property?: number;
    available?: boolean;
    page?: number;
  }): Promise<PaginatedResponse<Unit>> => {
    const response = await apiClient.get<PaginatedResponse<Unit>>('/properties/units/', {
      params,
    });
    return response.data;
  },

  /**
   * Get unit by ID
   */
  getUnit: async (id: number): Promise<Unit> => {
    const response = await apiClient.get<Unit>(`/properties/units/${id}/`);
    return response.data;
  },

  /**
   * Create new unit
   */
  createUnit: async (data: Partial<Unit>): Promise<Unit> => {
    const response = await apiClient.post<Unit>('/properties/units/', data);
    return response.data;
  },

  /**
   * Update unit
   */
  updateUnit: async (id: number, data: Partial<Unit>): Promise<Unit> => {
    const response = await apiClient.put<Unit>(`/properties/units/${id}/`, data);
    return response.data;
  },
};

