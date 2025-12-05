import io
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from dotenv import load_dotenv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
import torch
import re

# Load environment variables from .env
load_dotenv()

# Initialize BERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
model = AutoModel.from_pretrained('bert-base-uncased')

# Flask app initialization
app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5173",
    "https://me-profiled-frontend.vercel.app"
])

# PDF text extraction
def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

# Get BERT embeddings for text
def get_bert_embeddings(text):
    # Tokenize and encode
    inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=512, padding=True)
    
    # Get model output
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Use mean pooling on token embeddings
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.numpy()

# Extract keywords from text
def extract_keywords(text):
    # Simple keyword extraction - lowercase and split
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s+#]', ' ', text)
    words = set(text.split())
    # Filter out common words (basic stop words)
    stop_words = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
                  'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                  'can', 'could', 'may', 'might', 'must', 'and', 'or', 'but', 'in', 
                  'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'that'}
    return words - stop_words

# Detect experience level from resume
def detect_experience_level(resume_text):
    text_lower = resume_text.lower()
    
    # Keywords for different experience levels
    intern_keywords = ['intern', 'internship', 'student', 'currently pursuing', 'expected graduation', 
                       'undergraduate', 'college student', 'university student', 'seeking internship']
    fresher_keywords = ['fresher', 'recent graduate', 'entry level', 'no experience', 'graduated in', 
                        'bachelor', 'degree in', 'just completed', 'newly graduated']
    
    # Check for year patterns (e.g., "2019-2023", "3 years", "5+ years")
    year_pattern = r'(\d+)\s*(?:\+)?\s*years?'
    years_match = re.findall(year_pattern, text_lower)
    
    # Count experience indicators
    experience_years = [int(y) for y in years_match if int(y) < 50]  # Filter out year dates
    max_years = max(experience_years) if experience_years else 0
    
    # Check for intern/fresher keywords
    intern_count = sum(1 for keyword in intern_keywords if keyword in text_lower)
    fresher_count = sum(1 for keyword in fresher_keywords if keyword in text_lower)
    
    # Determine experience level
    if intern_count >= 2 or 'internship' in text_lower:
        return 'intern'
    elif fresher_count >= 1 or (max_years == 0 and 'graduate' in text_lower):
        return 'fresher'
    elif max_years >= 3:
        return 'experienced'
    elif max_years > 0 and max_years < 3:
        return 'fresher'
    else:
        # Default based on content length and keywords
        work_indicators = ['company', 'project', 'developed', 'managed', 'led', 'implemented']
        work_count = sum(1 for word in work_indicators if word in text_lower)
        return 'experienced' if work_count >= 5 else 'fresher'

# Calculate match scores
def calculate_match_score(resume_text, job_description, experience_level='auto'):
    # Get embeddings
    resume_emb = get_bert_embeddings(resume_text)
    job_emb = get_bert_embeddings(job_description)
    
    # Calculate semantic similarity (0 to 1)
    semantic_similarity = cosine_similarity(resume_emb, job_emb)[0][0]
    
    # Extract keywords
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)
    
    # Calculate keyword match
    common_keywords = resume_keywords.intersection(job_keywords)
    keyword_match = len(common_keywords) / len(job_keywords) if len(job_keywords) > 0 else 0
    
    # Adjust weights based on experience level
    if experience_level == 'intern':
        # For interns: focus more on skills and keywords, less on experience
        skills_weight = 0.60
        experience_weight = 0.20
        keyword_weight = 0.20
        skills_match = int((semantic_similarity * 0.5 + keyword_match * 0.5) * 100)
    elif experience_level == 'fresher':
        # For freshers: balance skills and keywords, moderate experience
        skills_weight = 0.55
        experience_weight = 0.30
        keyword_weight = 0.15
        skills_match = int((semantic_similarity * 0.6 + keyword_match * 0.4) * 100)
    else:  # experienced
        # For experienced: traditional weighting
        skills_weight = 0.50
        experience_weight = 0.40
        keyword_weight = 0.10
        skills_match = int((semantic_similarity * 0.7 + keyword_match * 0.3) * 100)
    
    # Experience match: based on semantic similarity
    experience_match = int(semantic_similarity * 100)
    
    # Keyword match percentage
    keyword_match_percent = int(keyword_match * 100)
    
    # Final score calculation with adjusted weights
    match_score = int((skills_match * skills_weight) + (experience_match * experience_weight) + (keyword_match_percent * keyword_weight))
    
    return match_score, skills_match, experience_match, keyword_match_percent, common_keywords

# Generate analysis based on scores
def generate_analysis(match_score, skills_match, experience_match, keyword_match, common_keywords, resume_text, job_description, experience_level='auto'):
    # Generate summary based on experience level
    level_label = experience_level.capitalize()
    if match_score >= 85:
        summary = f"Strong match with {match_score}% overall compatibility. As a {level_label}, the candidate's profile aligns well with the job requirements and demonstrates relevant expertise."
    elif match_score >= 70:
        summary = f"Moderate match with {match_score}% overall compatibility. As a {level_label}, the candidate shows good potential with some areas that could be enhanced to better align with the role."
    else:
        summary = f"Developing match with {match_score}% overall compatibility. As a {level_label}, the candidate has foundational qualities but would benefit from developing additional skills and experience for this role."
    
    # Generate strengths based on experience level
    strengths = []
    if experience_level == 'intern':
        if skills_match >= 60:
            strengths.append("Good foundational technical skills for an internship role")
        if keyword_match >= 40:
            strengths.append("Demonstrates awareness of relevant technologies and tools")
        if len(common_keywords) > 5:
            strengths.append(f"Shows familiarity with {len(common_keywords)} key terms from the job posting")
        strengths.append("Eager to learn and grow in the field")
    elif experience_level == 'fresher':
        if skills_match >= 65:
            strengths.append("Solid technical skills for an entry-level candidate")
        if keyword_match >= 50:
            strengths.append("Good understanding of relevant technologies and frameworks")
        if len(common_keywords) > 8:
            strengths.append(f"Familiar with {len(common_keywords)} important industry keywords")
        if experience_match >= 60:
            strengths.append("Shows academic or project experience relevant to the role")
    else:  # experienced
        if skills_match >= 75:
            strengths.append("Strong technical skills alignment with job requirements")
        if experience_match >= 75:
            strengths.append("Relevant work experience matching the role's expectations")
        if keyword_match >= 60:
            strengths.append("Good coverage of key technologies and tools mentioned in job description")
        if len(common_keywords) > 10:
            strengths.append(f"Demonstrates knowledge of {len(common_keywords)} relevant keywords and technologies")
    
    if not strengths:
        strengths.append("Shows foundational knowledge in the field")
    
    # Generate areas for improvement based on experience level
    improvements = []
    if experience_level == 'intern':
        if skills_match < 60:
            improvements.append("Build foundational skills in the key technologies mentioned in the job description")
        if keyword_match < 40:
            improvements.append("Learn and include relevant technical keywords in your resume")
        improvements.append("Highlight academic projects and coursework related to the role")
        improvements.append("Add any relevant certifications or online courses completed")
    elif experience_level == 'fresher':
        if skills_match < 65:
            improvements.append("Strengthen technical skills to better align with job requirements")
        if keyword_match < 50:
            improvements.append("Include more technologies and tools mentioned in the job posting")
        improvements.append("Emphasize personal projects and academic achievements")
        if experience_match < 60:
            improvements.append("Add more details about relevant coursework and hands-on experience")
    else:  # experienced
        if skills_match < 75:
            improvements.append("Enhance technical skills section to better match job requirements")
        if experience_match < 75:
            improvements.append("Highlight more relevant work experience and projects related to the role")
        if keyword_match < 60:
            improvements.append("Include more specific technologies, tools, and frameworks mentioned in the job description")
        if len(common_keywords) < 10:
            improvements.append("Add industry-specific keywords and technical terminology from the job posting")
    
    improvements.append("Tailor resume content to emphasize achievements that directly relate to job responsibilities")
    
    return {
        "matchScore": match_score,
        "skillsMatchPercent": skills_match,
        "experienceMatchPercent": experience_match,
        "keywordMatchPercent": keyword_match,
        "experienceLevel": experience_level,
        "summary": summary,
        "strengths": strengths[:5],  # Limit to 5
        "areasForImprovement": improvements[:5]  # Limit to 5
    }

# AI resume analyzer endpoint
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Hello from Backend"}), 200

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400

    job_description = request.form.get('jobDescription', '')
    if not job_description:
        return jsonify({'error': 'No job description provided'}), 400

    # Get experience level from request or detect automatically
    experience_level = request.form.get('experienceLevel', 'auto')

    resume_file = request.files['resume']
    resume_text = extract_text_from_pdf(io.BytesIO(resume_file.read()))

    if not resume_text:
        return jsonify({'error': 'Could not extract text from the resume PDF. The file might be empty, corrupted, or image-based.'}), 500

    try:
        # Auto-detect experience level if not provided
        if experience_level == 'auto':
            experience_level = detect_experience_level(resume_text)
        
        # Calculate match scores using BERT with experience level
        match_score, skills_match, experience_match, keyword_match, common_keywords = calculate_match_score(
            resume_text, job_description, experience_level
        )
        
        # Generate detailed analysis with experience level
        analysis_result = generate_analysis(
            match_score, skills_match, experience_match, keyword_match, 
            common_keywords, resume_text, job_description, experience_level
        )

        return jsonify(analysis_result)

    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        return jsonify({'error': f'Failed to analyze resume: {str(e)}'}), 500

# Start server
if __name__ == '__main__':
    app.run(debug=True, port=5001)
