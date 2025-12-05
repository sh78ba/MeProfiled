"""
Text processing utilities
"""
import re


def extract_keywords(text):
    """
    Extract keywords from text with stop word filtering
    
    Args:
        text: Input text string
        
    Returns:
        set: Set of keywords
    """
    # Simple keyword extraction - lowercase and split
    text = text.lower()
    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s+#]', ' ', text)
    words = set(text.split())
    
    # Filter out common words (basic stop words)
    stop_words = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
        'can', 'could', 'may', 'might', 'must', 'and', 'or', 'but', 'in', 
        'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'that'
    }
    
    return words - stop_words


def detect_experience_level(resume_text):
    """
    Detect experience level from resume text
    
    Args:
        resume_text: Resume text string
        
    Returns:
        str: Experience level ('intern', 'fresher', or 'experienced')
    """
    text_lower = resume_text.lower()
    
    # Keywords for different experience levels
    intern_keywords = [
        'intern', 'internship', 'student', 'currently pursuing', 
        'expected graduation', 'undergraduate', 'college student', 
        'university student', 'seeking internship'
    ]
    fresher_keywords = [
        'fresher', 'recent graduate', 'entry level', 'no experience', 
        'graduated in', 'bachelor', 'degree in', 'just completed', 
        'newly graduated'
    ]
    
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
