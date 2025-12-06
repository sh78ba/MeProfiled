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
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', '*').split(',')
    CORS_MAX_AGE = 3600
    
    # Model settings - production-grade model for Hugging Face Spaces (16GB RAM)
    MODEL_NAME = os.getenv('MODEL_NAME', 'sentence-transformers/all-mpnet-base-v2')  # 420MB production model
    MAX_TEXT_LENGTH = 5000  # 5000 characters
    MAX_SEQUENCE_LENGTH = 512  # 512 tokens
    EMBEDDINGS_CACHE_SIZE = 32  # LRU cache for embeddings
    
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
