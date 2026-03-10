from sqlalchemy import Column, Integer, String, Text, Float, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base

class ResumeAnalysis(Base):
    __tablename__ = "resume_analysis"
    
    id = Column(Integer, primary_key=True, index=True)
    resume_text = Column(Text, nullable=False)
    job_description = Column(Text, nullable=False)
    fit_score = Column(Float, nullable=False)
    fit_category = Column(String(20), nullable=False)
    similarity_score = Column(Float, nullable=False)
    skill_match_score = Column(Float, nullable=False)
    matched_skills = Column(JSON, nullable=False)
    missing_skills = Column(JSON, nullable=False)
    ai_feedback = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "resume_text": self.resume_text,
            "job_description": self.job_description,
            "fit_score": self.fit_score,
            "fit_category": self.fit_category,
            "similarity_score": self.similarity_score,
            "skill_match_score": self.skill_match_score,
            "matched_skills": self.matched_skills,
            "missing_skills": self.missing_skills,
            "ai_feedback": self.ai_feedback,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
