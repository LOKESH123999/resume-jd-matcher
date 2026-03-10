from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import logging

from ..database import get_db
from ..models import ResumeAnalysis
from ..schemas import ResumeMatchRequest, ResumeMatchResponse, ResumeAnalysisResponse, ErrorResponse
from ..services.matcher_service import MatcherService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["resume-matcher"])
matcher_service = MatcherService()

@router.post("/analyze", response_model=ResumeMatchResponse)
async def analyze_resume_match(
    request: ResumeMatchRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Analyze resume against job description and provide matching analysis
    """
    try:
        logger.info(f"Received analysis request")
        
        # Perform analysis
        result = matcher_service.analyze_resume_job_match(
            resume_text=request.resume_text,
            job_text=request.job_description
        )
        
        if not result.get("success"):
            raise HTTPException(
                status_code=400,
                detail=result.get("error", "Analysis failed")
            )
        
        # Save analysis to database in background
        background_tasks.add_task(
            save_analysis_to_db,
            db=db,
            resume_text=request.resume_text,
            job_description=request.job_description,
            analysis_result=result
        )
        
        # Return response
        return ResumeMatchResponse(
            success=True,
            score_breakdown=result["score_breakdown"],
            skills=result["skills"],
            ai_feedback=result["ai_feedback"],
            analysis_id=None  # Will be populated after background save
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during analysis"
        )

@router.get("/analyses", response_model=List[ResumeAnalysisResponse])
async def get_all_analyses(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get all saved resume analyses (paginated)
    """
    try:
        analyses = db.query(ResumeAnalysis).order_by(
            ResumeAnalysis.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        return analyses
        
    except Exception as e:
        logger.error(f"Error fetching analyses: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch analyses"
        )

@router.get("/analyses/{analysis_id}", response_model=ResumeAnalysisResponse)
async def get_analysis_by_id(analysis_id: int, db: Session = Depends(get_db)):
    """
    Get specific analysis by ID
    """
    try:
        analysis = db.query(ResumeAnalysis).filter(
            ResumeAnalysis.id == analysis_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail="Analysis not found"
            )
        
        return analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching analysis {analysis_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch analysis"
        )

@router.delete("/analyses/{analysis_id}")
async def delete_analysis(analysis_id: int, db: Session = Depends(get_db)):
    """
    Delete analysis by ID
    """
    try:
        analysis = db.query(ResumeAnalysis).filter(
            ResumeAnalysis.id == analysis_id
        ).first()
        
        if not analysis:
            raise HTTPException(
                status_code=404,
                detail="Analysis not found"
            )
        
        db.delete(analysis)
        db.commit()
        
        return {"message": "Analysis deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting analysis {analysis_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete analysis"
        )

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "Resume-Job Description Matcher",
        "version": "1.0.0"
    }

# Background task function
def save_analysis_to_db(
    db: Session,
    resume_text: str,
    job_description: str,
    analysis_result: dict
):
    """
    Save analysis result to database
    """
    try:
        analysis = ResumeAnalysis(
            resume_text=resume_text,
            job_description=job_description,
            fit_score=analysis_result["score_breakdown"]["score"],
            fit_category=analysis_result["score_breakdown"]["category"],
            similarity_score=analysis_result["score_breakdown"]["similarity_score"],
            skill_match_score=analysis_result["score_breakdown"]["skill_match_score"],
            matched_skills=analysis_result["skills"]["matched_skills"],
            missing_skills=analysis_result["skills"]["missing_skills"],
            ai_feedback=analysis_result["ai_feedback"]
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        logger.info(f"Analysis saved to database with ID: {analysis.id}")
        
    except Exception as e:
        logger.error(f"Error saving analysis to database: {str(e)}")
        db.rollback()
