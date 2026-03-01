import axios from 'axios';
import { ChatResponse, HealthStatus } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 2 minutes timeout
});

export const api = {
  async sendMessage(message: string, file?: File): Promise<string> {
    const formData = new FormData();
    formData.append('message', message);

    if (file) {
      formData.append('file', file);
    }

    const response = await axios.post<ChatResponse>(
      `${API_BASE_URL}/chat`,
      formData,
      {
        withCredentials: true,
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 600000, // 10 minutes for long-running processes
      }
    );

    return response.data.response;
  },

  async getHealth(): Promise<HealthStatus> {
    const response = await apiClient.get<HealthStatus>('/health');
    return response.data;
  },

  async getInfo(): Promise<{ name: string; version: string; docs: string }> {
    const response = await apiClient.get('/');
    return response.data;
  },
};
