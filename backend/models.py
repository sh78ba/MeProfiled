"""
Sentence transformer model management and embeddings generation
"""
import os
import gc
from functools import lru_cache
from sentence_transformers import SentenceTransformer
from config import get_config

config = get_config()

# Set cache directories for serverless
os.environ.setdefault('TRANSFORMERS_CACHE', '/tmp/transformers')
os.environ.setdefault('HF_HOME', '/tmp/huggingface')

# Global variable for model caching
_model = None


def get_model():
    """
    Get sentence transformer model with lazy loading and memory optimization
    
    Returns:
        SentenceTransformer: Loaded model
    """
    global _model
    if _model is None:
        print(f"Loading sentence transformer model: {config.MODEL_NAME}...")
        _model = SentenceTransformer(
            config.MODEL_NAME,
            device='cpu',  # Force CPU to reduce memory
            cache_folder='/tmp/transformers'  # Use tmp for serverless
        )
        # Force garbage collection after loading
        gc.collect()
        print("Model loaded successfully")
    return _model


@lru_cache(maxsize=128)
def get_bert_embeddings_cached(text_hash):
    """
    Cached version of get_bert_embeddings
    
    Args:
        text_hash: Hash of the text (for caching)
        
    Returns:
        numpy.ndarray: Text embeddings
    """
    return get_bert_embeddings(text_hash)


def get_bert_embeddings(text):
    """
    Generate embeddings for text using sentence transformers
    
    Args:
        text: Input text string
        
    Returns:
        numpy.ndarray: Text embeddings (2D array)
        
    Raises:
        Exception: If embedding generation fails
    """
    try:
        model = get_model()
        
        # Truncate text if too long
        if len(text) > config.MAX_TEXT_LENGTH:
            text = text[:config.MAX_TEXT_LENGTH]
        
        # Generate embeddings (sentence-transformers handles tokenization internally)
        embeddings = model.encode(text, convert_to_numpy=True, show_progress_bar=False)
        
        # Force garbage collection to free memory
        gc.collect()
        
        # Reshape to 2D array for consistency with sklearn
        return embeddings.reshape(1, -1)
    except Exception as e:
        print(f"Error generating embeddings: {str(e)}")
        raise


def preload_model():
    """
    Pre-load the model (useful for production)
    """
    print("Pre-loading sentence transformer model...")
    get_model()
    print("Model pre-loaded successfully")
