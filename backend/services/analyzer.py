"""
Resume analysis service
"""
from sklearn.metrics.pairwise import cosine_similarity
from models import get_bert_embeddings
from utils import extract_keywords


def calculate_match_score(resume_text, job_description, experience_level='auto'):
    """
    Calculate match scores between resume and job description
    
    Args:
        resume_text: Resume text string
        job_description: Job description text string
        experience_level: Experience level ('intern', 'fresher', 'experienced', or 'auto')
        
    Returns:
        tuple: (match_score, skills_match, experience_match, keyword_match_percent, common_keywords)
    """
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
    match_score = int(
        (skills_match * skills_weight) + 
        (experience_match * experience_weight) + 
        (keyword_match_percent * keyword_weight)
    )
    
    return match_score, skills_match, experience_match, keyword_match_percent, common_keywords


def generate_analysis(match_score, skills_match, experience_match, keyword_match, 
                     common_keywords, resume_text, job_description, experience_level='auto'):
    """
    Generate detailed analysis based on scores
    
    Args:
        match_score: Overall match score (0-100)
        skills_match: Skills match percentage
        experience_match: Experience match percentage
        keyword_match: Keyword match percentage
        common_keywords: Set of common keywords
        resume_text: Resume text (for reference)
        job_description: Job description text (for reference)
        experience_level: Experience level
        
    Returns:
        dict: Analysis results
    """
    # Generate summary based on experience level
    level_label = experience_level.capitalize()
    if match_score >= 85:
        summary = f"Strong match with {match_score}% overall compatibility. As a {level_label}, the candidate's profile aligns well with the job requirements and demonstrates relevant expertise."
    elif match_score >= 70:
        summary = f"Moderate match with {match_score}% overall compatibility. As a {level_label}, the candidate shows good potential with some areas that could be enhanced to better align with the role."
    else:
        summary = f"Developing match with {match_score}% overall compatibility. As a {level_label}, the candidate has foundational qualities but would benefit from developing additional skills and experience for this role."
    
    # Generate strengths based on experience level
    strengths = _generate_strengths(skills_match, experience_match, keyword_match, 
                                   common_keywords, experience_level)
    
    # Generate areas for improvement based on experience level
    improvements = _generate_improvements(skills_match, experience_match, keyword_match, 
                                        common_keywords, experience_level)
    
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


def _generate_strengths(skills_match, experience_match, keyword_match, common_keywords, experience_level):
    """Generate strengths list based on experience level"""
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
    
    return strengths


def _generate_improvements(skills_match, experience_match, keyword_match, common_keywords, experience_level):
    """Generate improvements list based on experience level"""
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
    
    return improvements
