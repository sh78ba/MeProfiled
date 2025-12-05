"""
Resume analysis service
"""
from sklearn.metrics.pairwise import cosine_similarity
from models import get_bert_embeddings
from utils import extract_keywords


def calculate_match_score(resume_text, job_description, experience_level='auto'):
    """
    Calculate match scores between resume and job description with improved algorithm
    
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
    
    # Boost semantic similarity (accounts for model limitations)
    # Apply sigmoid-like boosting to make scores more realistic
    boosted_similarity = 1 / (1 + pow(2.718, -5 * (semantic_similarity - 0.5)))
    
    # Extract keywords with enhanced extraction
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_description)
    
    # Calculate keyword match with partial matching
    common_keywords = resume_keywords.intersection(job_keywords)
    
    # Partial keyword matching (for variations like "python" vs "python3")
    partial_matches = set()
    for jk in job_keywords:
        for rk in resume_keywords:
            if len(jk) > 3 and len(rk) > 3:
                if jk in rk or rk in jk:
                    partial_matches.add(jk)
    
    common_keywords.update(partial_matches)
    keyword_match = len(common_keywords) / len(job_keywords) if len(job_keywords) > 0 else 0
    
    # Adjust weights based on experience level
    if experience_level == 'intern':
        # For interns: prioritize projects and skills (70% combined)
        skills_weight = 0.55
        experience_weight = 0.15
        keyword_weight = 0.30
        # Skills calculation emphasizes keyword match heavily for interns
        skills_match = int((boosted_similarity * 0.35 + keyword_match * 0.65) * 100)
    elif experience_level == 'fresher':
        # For freshers: projects and internship experience (60% combined)
        skills_weight = 0.40
        experience_weight = 0.40
        keyword_weight = 0.20
        skills_match = int((boosted_similarity * 0.45 + keyword_match * 0.55) * 100)
    else:  # experienced
        # For experienced: work experience is primary (55%)
        skills_weight = 0.35
        experience_weight = 0.55
        keyword_weight = 0.10
        skills_match = int((boosted_similarity * 0.70 + keyword_match * 0.30) * 100)
    
    # Experience match with boosting
    experience_match = int(boosted_similarity * 100)
    
    # Keyword match percentage
    keyword_match_percent = int(keyword_match * 100)
    
    # Final score calculation with adjusted weights
    match_score = int(
        (skills_match * skills_weight) + 
        (experience_match * experience_weight) + 
        (keyword_match_percent * keyword_weight)
    )
    
    # Apply reasonable floor/ceiling
    match_score = max(30, min(95, match_score))  # Keep between 30-95%
    
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
        if skills_match >= 55:
            strengths.append("Strong project-based technical skills demonstrated")
        if keyword_match >= 35:
            strengths.append("Good familiarity with relevant technologies and tools")
        if len(common_keywords) > 4:
            strengths.append(f"Shows knowledge of {len(common_keywords)} key technical skills from the job posting")
        if skills_match >= 60:
            strengths.append("Projects showcase practical application of relevant technologies")
        strengths.append("Demonstrates strong learning potential and technical foundation")
    elif experience_level == 'fresher':
        if skills_match >= 60:
            strengths.append("Solid technical skills with hands-on project experience")
        if experience_match >= 55:
            strengths.append("Good internship or academic project experience relevant to the role")
        if keyword_match >= 45:
            strengths.append("Demonstrates understanding of key technologies and frameworks")
        if len(common_keywords) > 7:
            strengths.append(f"Familiar with {len(common_keywords)} important technologies mentioned in job description")
        if experience_match >= 65:
            strengths.append("Projects and internships align well with job requirements")
    else:  # experienced
        if experience_match >= 70:
            strengths.append("Strong relevant work experience matching the role's expectations")
        if skills_match >= 70:
            strengths.append("Excellent technical skills alignment with job requirements")
        if experience_match >= 75:
            strengths.append("Proven track record in similar roles and responsibilities")
        if keyword_match >= 55:
            strengths.append("Good coverage of key technologies and tools mentioned in job description")
        if len(common_keywords) > 10:
            strengths.append(f"Demonstrates expertise in {len(common_keywords)} relevant keywords and technologies")
    
    if not strengths:
        strengths.append("Shows foundational knowledge in the field")
    
    return strengths


def _generate_improvements(skills_match, experience_match, keyword_match, common_keywords, experience_level):
    """Generate improvements list based on experience level"""
    improvements = []
    
    if experience_level == 'intern':
        if skills_match < 55:
            improvements.append("Add more technical projects showcasing skills mentioned in the job description")
        if keyword_match < 35:
            improvements.append("Include relevant technical skills and tools from the job posting in your projects section")
        improvements.append("Highlight 2-3 strong projects with specific technologies and outcomes")
        improvements.append("Emphasize coursework and certifications relevant to the role")
        if len(common_keywords) < 5:
            improvements.append("Learn and demonstrate key technologies mentioned in the job requirements")
    elif experience_level == 'fresher':
        if experience_match < 55:
            improvements.append("Add more details about internships, projects, and hands-on experience")
        if skills_match < 60:
            improvements.append("Strengthen project descriptions with specific technologies and measurable outcomes")
        if keyword_match < 45:
            improvements.append("Include more technologies and frameworks mentioned in the job posting")
        improvements.append("Emphasize practical experience from internships and personal projects")
        if len(common_keywords) < 8:
            improvements.append("Highlight experience with key tools and technologies from the job description")
    else:  # experienced
        if experience_match < 70:
            improvements.append("Highlight more relevant work experience and accomplishments related to the role")
        if skills_match < 70:
            improvements.append("Emphasize technical expertise in areas mentioned in the job requirements")
        if keyword_match < 55:
            improvements.append("Include more specific technologies, tools, and frameworks mentioned in the job description")
        if experience_match < 75:
            improvements.append("Add quantifiable achievements from previous roles that align with job responsibilities")
        if len(common_keywords) < 10:
            improvements.append("Add industry-specific keywords and technical terminology from the job posting")
    
    improvements.append("Tailor resume content to emphasize achievements that directly relate to job responsibilities")
    
    return improvements
