"""
API routes for the application
"""
import io
from datetime import datetime
from flask import Blueprint, request, jsonify
from config import get_config
from utils import validate_pdf, extract_text_from_pdf, get_secure_filename, detect_experience_level
from services import calculate_match_score, generate_analysis

config = get_config()# Create blueprint
api = Blueprint('api', __name__)


@api.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({"message": "Hello from Backend"}), 200


@api.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        from models import get_model
        # Check if model is loaded
        model = get_model()
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'model_loaded': True
        }), 200
    except Exception as e:
        print(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 503


@api.route('/analyze', methods=['POST'])
def analyze_resume():
    """
    Analyze resume against job description
    
    Expected form data:
        - resume: PDF file
        - jobDescription: Text string
        - experienceLevel: 'auto', 'intern', 'fresher', or 'experienced' (optional)
        
    Returns:
        JSON with analysis results
    """
    start_time = datetime.now()
    
    try:
        # Validate file upload
        if 'resume' not in request.files:
            print("No resume file in request")
            return jsonify({'error': 'No resume file provided'}), 400

        resume_file = request.files['resume']
        
        # Validate filename
        if resume_file.filename == '':
            print("Empty filename")
            return jsonify({'error': 'No file selected'}), 400
        
        if not validate_pdf(resume_file.filename):
            print(f"Invalid file type: {resume_file.filename}")
            return jsonify({'error': 'Only PDF files are allowed'}), 400

        # Validate job description
        job_description = request.form.get('jobDescription', '').strip()
        if not job_description:
            print("No job description provided")
            return jsonify({'error': 'No job description provided'}), 400
        
        if len(job_description) < config.MIN_JOB_DESCRIPTION_LENGTH:
            print("Job description too short")
            return jsonify({
                'error': f'Job description must be at least {config.MIN_JOB_DESCRIPTION_LENGTH} characters'
            }), 400
        
        if len(job_description) > config.MAX_JOB_DESCRIPTION_LENGTH:
            print("Job description too long")
            return jsonify({
                'error': f'Job description must be less than {config.MAX_JOB_DESCRIPTION_LENGTH} characters'
            }), 400

        # Get and validate experience level
        experience_level = request.form.get('experienceLevel', 'auto').lower()
        if experience_level not in config.VALID_EXPERIENCE_LEVELS:
            print(f"Invalid experience level: {experience_level}")
            experience_level = 'auto'

        # Extract text from PDF
        print(f"Processing resume: {get_secure_filename(resume_file.filename)}")
        resume_text = extract_text_from_pdf(io.BytesIO(resume_file.read()))

        if not resume_text:
            print("Failed to extract text from PDF")
            return jsonify({
                'error': 'Could not extract text from the resume PDF. The file might be empty, encrypted, image-based, or corrupted. Please ensure your PDF contains selectable text.'
            }), 400

        # Auto-detect experience level if not provided
        if experience_level == 'auto':
            experience_level = detect_experience_level(resume_text)
            print(f"Auto-detected experience level: {experience_level}")
        
        # Calculate match scores using BERT with experience level
        print("Calculating match scores...")
        match_score, skills_match, experience_match, keyword_match, common_keywords = calculate_match_score(
            resume_text, job_description, experience_level
        )
        
        # Generate detailed analysis with experience level
        print("Generating analysis...")
        analysis_result = generate_analysis(
            match_score, skills_match, experience_match, keyword_match, 
            common_keywords, resume_text, job_description, experience_level
        )
        
        # Log processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        print(f"Analysis completed in {processing_time:.2f} seconds")
        analysis_result['processingTime'] = round(processing_time, 2)

        return jsonify(analysis_result), 200

    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        return jsonify({
            'error': 'An unexpected error occurred during analysis. Please try again or contact support if the issue persists.',
            'details': str(e) if config.DEBUG else None
        }), 500
