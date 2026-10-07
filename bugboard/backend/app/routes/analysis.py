from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.analyzer import get_code_snippet, deterministic_analyze
import os

router = APIRouter(prefix="/api/bugs", tags=["analysis"])

@router.post("/{bug_id}/analyze", response_model=schemas.BugAnalysisOut)
def analyze_bug(bug_id: int, db: Session = Depends(get_db)):
    bug = db.query(models.Bug).filter(models.Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
        
    project = bug.project
    
    # Clean up previous analysis if exists
    if bug.analysis:
        db.delete(bug.analysis)
        db.commit()
        
    if not project.extracted_path:
        raise HTTPException(status_code=400, detail="Project source files not available")
        
    file_path = os.path.join(project.extracted_path, bug.affected_file.lstrip('/\\'))
    
    snippet = ""
    if bug.line_number is not None:
        snippet = get_code_snippet(file_path, bug.line_number)
        
    cause, fix, steps = deterministic_analyze(snippet if snippet else "")
    
    analysis = models.BugAnalysis(
        bug_id=bug.id,
        detected_snippet=snippet if snippet else None,
        potential_cause=cause,
        suggested_fix=fix,
        reproduction_steps=steps
    )
    
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis

@router.get("/{bug_id}/analysis", response_model=schemas.BugAnalysisOut)
def get_analysis(bug_id: int, db: Session = Depends(get_db)):
    analysis = db.query(models.BugAnalysis).filter(models.BugAnalysis.bug_id == bug_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
