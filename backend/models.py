"""
BERT model management and embeddings generation
"""
import torch
from functools import lru_cache
from transformers import AutoTokenizer, AutoModel
from config import get_config

config = get_config()

# Global variables for model caching
_tokenizer = None
_model = None


def get_model_and_tokenizer():
    """
    Get BERT model and tokenizer with lazy loading
    
    Returns:
        tuple: (tokenizer, model)
    """
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        print("Loading BERT model and tokenizer...")
        _tokenizer = AutoTokenizer.from_pretrained(config.MODEL_NAME)
        _model = AutoModel.from_pretrained(config.MODEL_NAME)
        _model.eval()  # Set to evaluation mode
        print("BERT model loaded successfully")
    return _tokenizer, _model


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
    Generate BERT embeddings for text
    
    Args:
        text: Input text string
        
    Returns:
        numpy.ndarray: Text embeddings
        
    Raises:
        Exception: If embedding generation fails
    """
    try:
        tokenizer, model = get_model_and_tokenizer()
        
        # Truncate text if too long
        if len(text) > config.MAX_TEXT_LENGTH:
            text = text[:config.MAX_TEXT_LENGTH]
        
        # Tokenize and encode
        inputs = tokenizer(
            text, 
            return_tensors='pt', 
            truncation=True, 
            max_length=config.MAX_SEQUENCE_LENGTH, 
            padding=True
        )
        
        # Get model output
        with torch.no_grad():
            outputs = model(**inputs)
        
        # Use mean pooling on token embeddings
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return embeddings.numpy()
    except Exception as e:
        print(f"Error generating embeddings: {str(e)}")
        raise


def preload_model():
    """
    Pre-load the BERT model (useful for production)
    """
    print("Pre-loading BERT model...")
    get_model_and_tokenizer()
    print("Model pre-loaded successfully")
