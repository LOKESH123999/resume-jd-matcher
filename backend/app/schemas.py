from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class ResumeMatchRequest(BaseModel):
    resume_text: str = Field(..., min_length=50, description="Resume text content")
    job_description: str = Field(..., min_length=50, description="Job description text")

class SkillMatch(BaseModel):
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    skill_match_score: float

class ScoreBreakdown(BaseModel):
    score: float
    category: str
    similarity_score: float
    skill_match_score: float

class AIFeedback(BaseModel):
    fit_analysis: str
    skills_to_learn: List[Dict[str, str]]
    learning_resources: List[Dict[str, str]]
    improvement_tip: str

class ResumeMatchResponse(BaseModel):
    success: bool
    score_breakdown: ScoreBreakdown
    skills: SkillMatch
    ai_feedback: AIFeedback
    analysis_id: Optional[int] = None

class ResumeAnalysisResponse(BaseModel):
    id: int
    resume_text: str
    job_description: str
    fit_score: float
    fit_category: str
    similarity_score: float
    skill_match_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    ai_feedback: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    message: Optional[str] = None
