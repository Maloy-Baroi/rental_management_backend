// User Types
export type UserRole = 'owner' | 'tenant' | 'admin';

export interface User {
  id: number;
  phone: string;
  email?: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse {
  user: User;
  tokens: AuthTokens;
}

export interface RegisterRequest {
  phone: string;
  email?: string;
  password: string;
  role: UserRole;
}

// Property Types
export interface Location {
  id: number;
  area_name?: string;
  village?: string;
  ward?: string;
  zone_or_union?: string;
  city_corporation?: string;
  upazila_or_thana?: string;
  district: string;
  division: string;
  country: string;
}

export interface Property {
  id: number;
  location: Location;
  house_name: string;
  age_of_building?: number;
  total_floors: number;
  has_lift: boolean;
  has_security_guard: boolean;
  has_parking: boolean;
  is_tiled: boolean;
  photos: string[];
  created_by: number;
  created_at: string;
  updated_at: string;
}

export interface Unit {
  id: number;
  property: number;
  unit_number: string;
  floor_number: number;
  facing: 'north' | 'south' | 'east' | 'west' | 'north_east' | 'north_west' | 'south_east' | 'south_west';
  bedrooms: number;
  bathrooms: number;
  area_sqft?: number;
  rent_amount: number;
  utility_charge?: number;
  is_available: boolean;
  description?: string;
  photos: string[];
  created_at: string;
  updated_at: string;
}

// Contract Types
export interface Contract {
  id: number;
  unit: number;
  tenant: number;
  start_date: string;
  end_date: string;
  rent_amount: number;
  security_deposit: number;
  status: 'active' | 'expired' | 'terminated';
  created_at: string;
  updated_at: string;
}

// Billing Types
export interface Bill {
  id: number;
  contract: number;
  billing_period_start: string;
  billing_period_end: string;
  rent_amount: number;
  utility_amount: number;
  total_amount: number;
  due_date: string;
  status: 'pending' | 'paid' | 'overdue' | 'cancelled';
  created_at: string;
  updated_at: string;
}

// Payment Types
export interface Payment {
  id: number;
  bill: number;
  amount: number;
  payment_method: 'bkash' | 'nagad' | 'rocket' | 'bank_transfer' | 'cash';
  transaction_id?: string;
  payment_date: string;
  status: 'completed' | 'pending' | 'failed';
  receipt_url?: string;
  created_at: string;
  updated_at: string;
}

// Dashboard Stats Types
export interface OwnerDashboardStats {
  total_properties: number;
  total_units: number;
  occupied_units: number;
  vacant_units: number;
  pending_rent_amount: number;
  pending_rent_count: number;
  total_tenants: number;
}

export interface TenantDashboardStats {
  current_contract?: Contract;
  next_payment?: {
    bill_id: number;
    amount: number;
    due_date: string;
    days_remaining: number;
  };
  total_paid: number;
  last_payment?: Payment;
}

// API Response Types
export interface ApiError {
  message: string;
  errors?: Record<string, string[]>;
}

export interface PaginatedResponse<T> {
  count: number;
  next?: string;
  previous?: string;
  results: T[];
}

