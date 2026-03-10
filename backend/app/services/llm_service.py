import os
import re
from groq import Groq
from typing import Dict, List, Any
import json

class LLMService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama3-70b-8192"  # Using Llama 3 for better analysis
        
        self.system_prompt = """
You are an expert career counselor and technical recruiter with 15+ years of experience in the tech industry.
You specialize in helping B.Tech CSE students in India improve their career prospects.

Analyze the resume-job match and provide actionable, honest feedback.
Be encouraging but realistic. Focus on practical advice that a 3rd-year student can implement.
Always provide specific, actionable recommendations.
"""
    
    def generate_user_prompt(self, resume_text: str, job_text: str, 
                           fit_score: float, skill_match_score: float,
                           matched_skills: List[str], missing_skills: List[str]) -> str:
        """Generate structured prompt for LLM analysis"""
        
        user_prompt = f"""
Analyze this resume-job description match:

OVERALL SCORES:
- Overall Fit Score: {fit_score}%
- Skill Match Score: {skill_match_score}%

SKILLS ANALYSIS:
Matched Skills: {', '.join(matched_skills) if matched_skills else 'None'}
Missing Skills: {', '.join(missing_skills) if missing_skills else 'None'}

RESUME TEXT:
{resume_text[:2000]}... [truncated for analysis]

JOB DESCRIPTION:
{job_text[:2000]}... [truncated for analysis]

Provide your analysis in this EXACT format:

1. **Why You Fit/Dont Fit**: [2-3 sentences explaining whether and why this candidate is a good match for the role]

2. **Top 3 Skills to Learn**: 
   - Skill 1: [skill name] - [brief explanation of why it's important for this role]
   - Skill 2: [skill name] - [brief explanation of why it's important for this role]
   - Skill 3: [skill name] - [brief explanation of why it's important for this role]

3. **Free Learning Resources**:
   - [Missing Skill 1]: [Specific Course/Resource Name] - [Platform] - [Direct link if possible, otherwise platform name]
   - [Missing Skill 2]: [Specific Course/Resource Name] - [Platform] - [Direct link if possible, otherwise platform name]
   - [Missing Skill 3]: [Specific Course/Resource Name] - [Platform] - [Direct link if possible, otherwise platform name]

4. **One Honest Improvement Tip**: [One specific, actionable advice that will make the biggest difference]

IMPORTANT GUIDELINES:
- Be honest but encouraging
- Focus on free/low-cost resources suitable for students
- Provide specific course names, not just platform names
- Keep responses concise but valuable
- If there are fewer than 3 missing skills, suggest related skills that would strengthen the profile
"""
        
        return user_prompt
    
    def parse_llm_response(self, response_text: str) -> Dict[str, Any]:
        """Parse structured LLM response into JSON format"""
        
        parsed_response = {
            "fit_analysis": "",
            "skills_to_learn": [],
            "learning_resources": [],
            "improvement_tip": ""
        }
        
        try:
            # Extract fit analysis
            fit_match = re.search(r'1\.\s*\*\*Why You Fit/Dont Fit\*\*:\s*(.*?)(?=\n\n|\n2\.)', response_text, re.DOTALL | re.IGNORECASE)
            if fit_match:
                parsed_response["fit_analysis"] = fit_match.group(1).strip()
            
            # Extract skills to learn
            skills_match = re.search(r'2\.\s*\*\*Top 3 Skills to Learn\*\*:\s*(.*?)(?=\n\n|\n3\.)', response_text, re.DOTALL | re.IGNORECASE)
            if skills_match:
                skills_text = skills_match.group(1).strip()
                skill_lines = re.findall(r'-\s*Skill\s*\d+:\s*([^-\n]+)', skills_text, re.IGNORECASE)
                
                for skill in skill_lines[:3]:
                    if ' - ' in skill:
                        parts = skill.split(' - ', 1)
                        skill_name = parts[0].strip()
                        importance = parts[1].strip() if len(parts) > 1 else ""
                        parsed_response["skills_to_learn"].append({
                            "skill": skill_name,
                            "importance": importance
                        })
            
            # Extract learning resources
            resources_match = re.search(r'3\.\s*\*\*Free Learning Resources\*\*:\s*(.*?)(?=\n\n|\n4\.)', response_text, re.DOTALL | re.IGNORECASE)
            if resources_match:
                resources_text = resources_match.group(1).strip()
                resource_lines = re.findall(r'-\s*([^-\n]+)', resources_text)
                
                for resource in resource_lines[:3]:
                    if ':' in resource:
                        parts = resource.split(':', 1)
                        skill = parts[0].strip()
                        resource_info = parts[1].strip() if len(parts) > 1 else ""
                        
                        if ' - ' in resource_info:
                            resource_parts = resource_info.split(' - ')
                            course_name = resource_parts[0].strip()
                            platform = resource_parts[1].strip() if len(resource_parts) > 1 else ""
                            link = resource_parts[2].strip() if len(resource_parts) > 2 else ""
                        else:
                            course_name = resource_info
                            platform = ""
                            link = ""
                        
                        parsed_response["learning_resources"].append({
                            "skill": skill,
                            "course": course_name,
                            "platform": platform,
                            "link": link
                        })
            
            # Extract improvement tip
            tip_match = re.search(r'4\.\s*\*\*One Honest Improvement Tip\*\*:\s*(.*?)(?=\n\n|$)', response_text, re.DOTALL | re.IGNORECASE)
            if tip_match:
                parsed_response["improvement_tip"] = tip_match.group(1).strip()
            
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            # Return default response on parsing error
            parsed_response = {
                "fit_analysis": "Analysis completed successfully. Please review the detailed scores and skill matches above.",
                "skills_to_learn": [
                    {"skill": "Technical Skills", "importance": "Focus on core technologies mentioned in the job description"},
                    {"skill": "Soft Skills", "importance": "Develop communication and teamwork abilities"},
                    {"skill": "Project Experience", "importance": "Build hands-on projects to demonstrate practical knowledge"}
                ],
                "learning_resources": [
                    {"skill": "Technical Skills", "course": "Free Code Camp", "platform": "freecodecamp.org", "link": ""},
                    {"skill": "Soft Skills", "course": "Communication Skills", "platform": "Coursera", "link": ""},
                    {"skill": "Project Experience", "course": "Build Projects", "platform": "GitHub", "link": ""}
                ],
                "improvement_tip": "Focus on building practical projects that demonstrate the key skills required for this role."
            }
        
        return parsed_response
    
    def analyze_match(self, resume_text: str, job_text: str, 
                     fit_score: float, skill_match_score: float,
                     matched_skills: List[str], missing_skills: List[str]) -> Dict[str, Any]:
        """Generate AI feedback using Groq API"""
        
        try:
            # Generate prompt
            user_prompt = self.generate_user_prompt(
                resume_text, job_text, fit_score, skill_match_score,
                matched_skills, missing_skills
            )
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
                top_p=1,
                stream=False
            )
            
            response_text = response.choices[0].message.content
            
            # Parse response
            parsed_feedback = self.parse_llm_response(response_text)
            
            return {
                "success": True,
                "feedback": parsed_feedback,
                "raw_response": response_text
            }
            
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return {
                "success": False,
                "error": str(e),
                "feedback": {
                    "fit_analysis": "AI analysis temporarily unavailable. Please review the scores and skill matches manually.",
                    "skills_to_learn": [],
                    "learning_resources": [],
                    "improvement_tip": "Try again later for AI-powered recommendations."
                }
            }
