import re
import string
from typing import List, Set

# Comprehensive tech skills database
TECH_SKILLS = {
    # Programming Languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift', 'kotlin',
    
    # Frontend Technologies
    'react', 'angular', 'vue', 'html', 'css', 'sass', 'tailwind', 'bootstrap', 'jquery', 'nextjs', 'nuxt',
    
    # Backend Technologies
    'nodejs', 'express', 'django', 'flask', 'spring', 'laravel', 'rails', 'fastapi', 'asp.net',
    
    # Databases
    'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'cassandra', 'elasticsearch',
    
    # Cloud & DevOps
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'ci/cd', 'git',
    
    # Data Science & AI
    'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'nlp', 'data analysis', 'pandas', 'numpy',
    'scikit-learn', 'data visualization', 'tableau', 'power bi', 'statistics',
    
    # Mobile Development
    'android', 'ios', 'flutter', 'react native', 'swift', 'kotlin', 'xamarin',
    
    # Other Technologies
    'api', 'rest', 'graphql', 'microservices', 'blockchain', 'web3', 'linux', 'ubuntu', 'windows',
    'agile', 'scrum', 'testing', 'unit testing', 'integration testing', 'ui/ux', 'figma'
}

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Convert to lowercase
    text = text.lower()
    # Remove special characters but keep spaces and alphanumeric
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_skills(text: str) -> List[str]:
    """Extract technical skills from text"""
    cleaned_text = clean_text(text)
    words = cleaned_text.split()
    
    found_skills = set()
    
    # Direct skill matching
    for skill in TECH_SKILLS:
        if skill in cleaned_text:
            found_skills.add(skill)
    
    # Partial matching for multi-word skills
    for skill in TECH_SKILLS:
        if ' ' in skill:  # Multi-word skills
            skill_words = skill.split()
            if all(word in words for word in skill_words):
                found_skills.add(skill)
    
    return list(found_skills)

def validate_text_length(text: str, min_length: int = 50) -> bool:
    """Validate if text meets minimum length requirement"""
    return len(text.strip()) >= min_length

def categorize_score(score: float) -> str:
    """Categorize score into High/Medium/Low"""
    if score >= 75:
        return "High"
    elif score >= 50:
        return "Medium"
    else:
        return "Low"
