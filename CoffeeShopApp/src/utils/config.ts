export const API_CONFIG = {
  BASE_URL: 'http://localhost:5001',
  TIMEOUT: 10000,
};
export const getApiUrl = (endpoint: string): string => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

export default API_CONFIG; 