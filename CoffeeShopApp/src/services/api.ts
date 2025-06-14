import axios, { AxiosInstance, AxiosResponse } from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  Coffee,
  CreateCoffeeRequest,
  UpdateCoffeeRequest,
  CreatePurchaseRequest,
  Purchase,
  User,
} from '../types';
import { API_CONFIG } from '../utils/config';

class ApiService {
  private api: AxiosInstance;

  constructor() {
    this.api = axios.create({
      baseURL: API_CONFIG.BASE_URL,
      timeout: API_CONFIG.TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.api.interceptors.request.use(
      async (config) => {
        const token = await AsyncStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          await AsyncStorage.removeItem('token');
          await AsyncStorage.removeItem('user');
        }
        return Promise.reject(error);
      }
    );
  }

  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response: AxiosResponse<AuthResponse> = await this.api.post('/auth/login', credentials);
    return response.data;
  }

  async register(userData: RegisterRequest): Promise<{ message: string }> {
    const response: AxiosResponse<{ message: string }> = await this.api.post('/auth/register', userData);
    return response.data;
  }

  async getCoffees(): Promise<Coffee[]> {
    const response: AxiosResponse<Coffee[]> = await this.api.get('/coffee/');
    return response.data;
  }

  async createCoffee(coffeeData: CreateCoffeeRequest): Promise<Coffee> {
    const response: AxiosResponse<Coffee> = await this.api.post('/coffee/', coffeeData);
    return response.data;
  }

  async updateCoffee(coffeeId: number, coffeeData: UpdateCoffeeRequest): Promise<Coffee> {
    const response: AxiosResponse<Coffee> = await this.api.put(`/coffee/${coffeeId}`, coffeeData);
    return response.data;
  }

  async deleteCoffee(coffeeId: number): Promise<{ message: string }> {
    const response: AxiosResponse<{ message: string }> = await this.api.delete(`/coffee/${coffeeId}`);
    return response.data;
  }

  async createPurchase(purchaseData: CreatePurchaseRequest): Promise<Purchase> {
    const response: AxiosResponse<Purchase> = await this.api.post('/purchase/', purchaseData);
    return response.data;
  }

  async getPurchaseHistory(): Promise<Purchase[]> {
    const response: AxiosResponse<Purchase[]> = await this.api.get('/purchase/');
    return response.data;
  }

  async setAuthToken(token: string): Promise<void> {
    await AsyncStorage.setItem('token', token);
  }

  async removeAuthToken(): Promise<void> {
    await AsyncStorage.removeItem('token');
  }

  async getAuthToken(): Promise<string | null> {
    return await AsyncStorage.getItem('token');
  }
}

export default new ApiService(); 