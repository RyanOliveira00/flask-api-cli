export interface User {
  id: number;
  username: string;
  email: string;
  is_admin: boolean;
  created_at: string;
  updated_at: string;
}

export interface Coffee {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  created_at?: string;
  updated_at?: string;
}

export interface CreateCoffeeRequest {
  name: string;
  description: string;
  price: number;
  stock: number;
}

export interface UpdateCoffeeRequest {
  name?: string;
  description?: string;
  price?: number;
  stock?: number;
}

export interface Purchase {
  id: number;
  user_id: number;
  coffee_id: number;
  quantity: number;
  total_price: number;
  created_at: string;
  updated_at: string;
  user?: User;
  coffee?: Coffee;
}

export interface CreatePurchaseRequest {
  coffee_id: number;
  quantity: number;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  is_admin?: boolean;
}

export interface AuthResponse {
  access_token: string;
}

export interface ApiResponse<T = any> {
  message?: string;
  error?: string;
  data?: T;
}

export type RootStackParamList = {
  Login: undefined;
  Register: undefined;
  Home: undefined;
  CoffeeList: undefined;
  AddCoffee: undefined;
  EditCoffee: { coffee: Coffee };
  PurchaseHistory: undefined;
  Profile: undefined;
};

export interface AuthContextType {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (userData: RegisterRequest) => Promise<void>;
  logout: () => Promise<void>;
  isLoading: boolean;
} 