"""
MeProfiled Backend Application - Modular Version
AI-powered resume analysis using BERT embeddings
"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import get_config
from routes import api
from models import preload_model

# Get configuration
config = get_config()

# Create Flask application
app = Flask(__name__)

# Apply configuration
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH
app.config['UPLOAD_EXTENSIONS'] = config.UPLOAD_EXTENSIONS

# Configure CORS with more permissive settings for production
CORS(app, 
     resources={r"/*": {
         "origins": config.ALLOWED_ORIGINS,
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type"],
         "expose_headers": ["Content-Type"],
         "supports_credentials": False,
         "max_age": config.CORS_MAX_AGE
     }})

# Register blueprints
app.register_blueprint(api)


# Error handlers
@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    return jsonify({'error': 'File size exceeds 16MB limit'}), 413


@app.errorhandler(404)
def not_found(error):
    """Handle not found error"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server error"""
    return jsonify({'error': 'Internal server error'}), 500


def create_app():
    """
    Application factory pattern
    
    Returns:
        Flask: Configured Flask application
    """
    return app


if __name__ == '__main__':
    print(f"Starting server on {config.HOST}:{config.PORT} (debug={config.DEBUG})")
    
    # Don't pre-load model to save memory - load on first request
    
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
