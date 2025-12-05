"""
Text processing utilities
"""
import re


def extract_keywords(text):
    """
    Extract keywords from text with enhanced stop word filtering and n-grams
    
    Args:
        text: Input text string
        
    Returns:
        set: Set of keywords including important phrases
    """
    text = text.lower()
    # Remove special characters but keep +, #, . for tech terms
    text = re.sub(r'[^a-zA-Z0-9\s+#\.]', ' ', text)
    
    # Extract single words
    words = text.split()
    
    # Enhanced stop words list
    stop_words = {
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
        'can', 'could', 'may', 'might', 'must', 'and', 'or', 'but', 'in', 
        'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'as', 'that',
        'this', 'these', 'those', 'it', 'its', 'about', 'into', 'through',
        'during', 'before', 'after', 'above', 'below', 'up', 'down', 'out',
        'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
        'there', 'when', 'where', 'why', 'how', 'all', 'both', 'each', 'few',
        'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
        'own', 'same', 'so', 'than', 'too', 'very', 'we', 'you', 'your',
        'our', 'their', 'his', 'her', 'my', 'me', 'him', 'them', 'us'
    }
    
    # Filter single words
    keywords = {w for w in words if len(w) > 2 and w not in stop_words}
    
    # Extract bigrams for technical terms (e.g., "machine learning", "data science")
    bigrams = [' '.join([words[i], words[i+1]]) 
               for i in range(len(words)-1) 
               if words[i] not in stop_words or words[i+1] not in stop_words]
    
    # Add meaningful bigrams (technical terms, skills)
    tech_patterns = [
        r'\b\w+\s+(learning|science|engineering|development|testing|management|analysis)\b',
        r'\b(machine|deep|data|web|mobile|software|full|front|back)\s+\w+\b',
        r'\b\w+\s+(js|py|sql|api|ui|ux|devops|cloud)\b'
    ]
    
    for pattern in tech_patterns:
        matches = re.findall(pattern, text)
        keywords.update(matches)
    
    # Add important bigrams
    for bigram in bigrams[:50]:  # Limit to avoid too many
        if any(tech in bigram for tech in ['learning', 'science', 'development', 'engineering', 'testing']):
            keywords.add(bigram)
    
    return keywords


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
