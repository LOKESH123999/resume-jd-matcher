from typing import Dict, List, Any
from .nlp_service import NLPService
from .llm_service import LLMService
from ..utils import extract_skills, categorize_score, validate_text_length

class MatcherService:
    def __init__(self):
        self.nlp_service = NLPService()
        self.llm_service = LLMService()
    
    def analyze_resume_job_match(self, resume_text: str, job_text: str) -> Dict[str, Any]:
        """Main service to analyze resume-job match"""
        
        # Validate inputs
        if not validate_text_length(resume_text) or not validate_text_length(job_text):
            return {
                "success": False,
                "error": "Both resume and job description must be at least 50 characters long"
            }
        
        try:
            # 1. Extract skills from both texts
            resume_skills = extract_skills(resume_text)
            job_skills = extract_skills(job_text)
            
            # 2. Calculate skill matches
            matched_skills = list(set(resume_skills) & set(job_skills))
            missing_skills = list(set(job_skills) - set(resume_skills))
            
            # Calculate skill match percentage
            skill_match_score = (len(matched_skills) / len(job_skills) * 100) if job_skills else 0
            
            # 3. Calculate text similarity using NLP
            similarity_score = self.nlp_service.calculate_similarity(resume_text, job_text)
            
            # 4. Calculate final weighted score
            final_score = (similarity_score * 0.6) + (skill_match_score * 0.4)
            final_score = round(final_score, 1)
            
            # 5. Categorize score
            fit_category = categorize_score(final_score)
            
            # 6. Generate AI feedback
            ai_analysis = self.llm_service.analyze_match(
                resume_text, job_text, final_score, skill_match_score,
                matched_skills, missing_skills
            )
            
            # 7. Build comprehensive response
            result = {
                "success": True,
                "score_breakdown": {
                    "score": final_score,
                    "category": fit_category,
                    "similarity_score": round(similarity_score, 1),
                    "skill_match_score": round(skill_match_score, 1)
                },
                "skills": {
                    "matched_skills": matched_skills,
                    "missing_skills": missing_skills,
                    "skill_match_score": round(skill_match_score, 1)
                },
                "ai_feedback": ai_analysis.get("feedback", {}),
                "analysis_summary": {
                    "total_skills_in_job": len(job_skills),
                    "skills_matched": len(matched_skills),
                    "skills_missing": len(missing_skills),
                    "resume_skill_count": len(resume_skills)
                }
            }
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Analysis failed: {str(e)}",
                "message": "Please try again with valid resume and job description text"
            }
    
    def get_skill_suggestions(self, missing_skills: List[str]) -> List[Dict[str, str]]:
        """Get learning suggestions for missing skills"""
        suggestions = []
        
        skill_resources = {
            "python": {
                "course": "Python for Everybody",
                "platform": "Coursera",
                "link": "https://www.coursera.org/specializations/python"
            },
            "react": {
                "course": "React - The Complete Guide",
                "platform": "Udemy",
                "link": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/"
            },
            "aws": {
                "course": "AWS Cloud Practitioner",
                "platform": "AWS Training",
                "link": "https://aws.amazon.com/training/"
            },
            "docker": {
                "course": "Docker Mastery",
                "platform": "Udemy",
                "link": "https://www.udemy.com/course/docker-mastery/"
            },
            "machine learning": {
                "course": "Machine Learning Specialization",
                "platform": "Coursera",
                "link": "https://www.coursera.org/specializations/machine-learning-introduction"
            }
        }
        
        for skill in missing_skills[:5]:  # Limit to top 5 missing skills
            skill_lower = skill.lower()
            resource = skill_resources.get(skill_lower, {
                "course": f"Learn {skill.title()}",
                "platform": "YouTube/Free Resources",
                "link": ""
            })
            
            suggestions.append({
                "skill": skill,
                "course": resource["course"],
                "platform": resource["platform"],
                "link": resource["link"]
            })
        
        return suggestions
