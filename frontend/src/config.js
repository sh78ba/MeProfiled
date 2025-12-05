// Environment configuration
const ENV = {
  development: {
    BACKEND_URL: 'http://localhost:5001',
  },
  production: {
    BACKEND_URL: import.meta.env.VITE_BACKEND_URL || 'https://sh78ba-meprofiled-backend.hf.space',
  },
};

const currentEnv = import.meta.env.MODE || 'production';

export const BACKEND_URL = ENV[currentEnv].BACKEND_URL;
export const isDevelopment = currentEnv === 'development';
export const isProduction = currentEnv === 'production';

// Backend model configuration: all-mpnet-base-v2 (420MB, state-of-the-art)
export const MODEL_CONFIG = {
  name: 'all-mpnet-base-v2',
  description: 'High-accuracy sentence transformer with enhanced semantic understanding',
  maxSequenceLength: 512,  // tokens
  maxTextLength: 5000,     // characters
  embeddingDimension: 768,
  qualityLevel: 'Production-grade',
};

// API configuration aligned with backend limits
export const API_CONFIG = {
  timeout: 300000, // 5 minutes (longer for complex analysis)
  initialLoadTime: 45000, // 45 seconds for first request
  maxFileSize: 16 * 1024 * 1024, // 16MB
  allowedFileTypes: ['application/pdf'],
  maxJobDescriptionLength: 10000,
  minJobDescriptionLength: 50,
  maxResumePagesRecommended: 20,
};

// Experience level options
export const EXPERIENCE_LEVELS = [
  { value: 'auto', label: 'Auto Detect', description: 'Let AI determine your level' },
  { value: 'intern', label: 'Intern', description: 'Student or intern position' },
  { value: 'fresher', label: 'Fresher (0-2 years)', description: 'Entry-level professional' },
  { value: 'experienced', label: 'Experienced (3+ years)', description: 'Mid to senior level' },
];

// User-friendly messages
export const MESSAGES = {
  FILE_TOO_LARGE: 'File size must be less than 16MB',
  INVALID_FILE_TYPE: 'Only PDF files are allowed',
  JOB_DESC_TOO_SHORT: 'Job description must be at least 50 characters',
  JOB_DESC_TOO_LONG: 'Job description must be less than 10,000 characters',
  NETWORK_ERROR: 'Unable to connect to server. The backend may be starting up (first request takes ~45 seconds). Please try again in a moment.',
  TIMEOUT_ERROR: 'Analysis is taking longer than expected with our advanced model. Please try again.',
  SERVER_STARTING: 'Server is starting up. Please wait 45 seconds and try again.',
  SERVER_ERROR: 'Server error occurred. Please try again.',
  ANALYZING: '🤖 Analyzing with advanced NLP model... This may take 30-60 seconds for detailed, accurate results.',
};
