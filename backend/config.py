"""
Configuration settings for the application
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_EXTENSIONS = ['.pdf']
    
    # Server settings
    PORT = int(os.getenv('PORT', 5001))
    HOST = '0.0.0.0'
    DEBUG = os.getenv('FLASK_ENV', 'production') == 'development'
    
    # CORS settings
    ALLOWED_ORIGINS = os.getenv(
        'ALLOWED_ORIGINS', 
        'http://localhost:5173,https://me-profiled-frontend.vercel.app'
    ).split(',')
    CORS_MAX_AGE = 3600
    
    # Model settings
    MODEL_NAME = os.getenv('MODEL_NAME', 'all-MiniLM-L6-v2')  # Better accuracy, still light (80MB)
    MAX_TEXT_LENGTH = 5000
    MAX_SEQUENCE_LENGTH = 512
    EMBEDDINGS_CACHE_SIZE = 128
    
    # Validation settings
    MIN_JOB_DESCRIPTION_LENGTH = 50
    MAX_JOB_DESCRIPTION_LENGTH = 10000
    MIN_RESUME_TEXT_LENGTH = 100
    MAX_PDF_PAGES = 20
    
    # Experience levels
    VALID_EXPERIENCE_LEVELS = ['auto', 'intern', 'fresher', 'experienced']
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}


def get_config():
    """Get configuration based on environment"""
    env = os.getenv('FLASK_ENV', 'production')
    return config.get(env, config['default'])
