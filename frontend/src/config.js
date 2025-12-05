// Environment configuration
const ENV = {
  development: {
    BACKEND_URL: 'http://localhost:5001',
  },
  production: {
    BACKEND_URL: import.meta.env.VITE_BACKEND_URL || 'https://your-backend-url.vercel.app',
  },
};

const currentEnv = import.meta.env.MODE || 'development';

export const BACKEND_URL = ENV[currentEnv].BACKEND_URL;
export const isDevelopment = currentEnv === 'development';
export const isProduction = currentEnv === 'production';

// API configuration
export const API_CONFIG = {
  timeout: 120000, // 2 minutes
  maxFileSize: 16 * 1024 * 1024, // 16MB
  allowedFileTypes: ['application/pdf'],
  maxJobDescriptionLength: 10000,
  minJobDescriptionLength: 50,
};
