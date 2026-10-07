from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(tags=["bugs"])

@router.post("/api/projects/{project_id}/bugs", response_model=schemas.BugOut)
def create_bug(project_id: int, bug: schemas.BugCreate, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db_bug = models.Bug(**bug.model_dump(), project_id=project_id)
    db.add(db_bug)
    db.commit()
    db.refresh(db_bug)
    return db_bug

@router.get("/api/projects/{project_id}/bugs", response_model=list[schemas.BugOut])
def get_project_bugs(project_id: int, db: Session = Depends(get_db)):
    return db.query(models.Bug).filter(models.Bug.project_id == project_id).all()

@router.get("/api/bugs/{bug_id}", response_model=schemas.BugOut)
def get_bug(bug_id: int, db: Session = Depends(get_db)):
    bug = db.query(models.Bug).filter(models.Bug.id == bug_id).first()
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    return bug

@router.put("/api/bugs/{bug_id}", response_model=schemas.BugOut)
def update_bug(bug_id: int, bug_update: schemas.BugUpdate, db: Session = Depends(get_db)):
    db_bug = db.query(models.Bug).filter(models.Bug.id == bug_id).first()
    if not db_bug:
        raise HTTPException(status_code=404, detail="Bug not found")

    update_data = bug_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_bug, key, value)

    db.commit()
    db.refresh(db_bug)
    return db_bug

@router.delete("/api/bugs/{bug_id}")
def delete_bug(bug_id: int, db: Session = Depends(get_db)):
    db_bug = db.query(models.Bug).filter(models.Bug.id == bug_id).first()
    if not db_bug:
        raise HTTPException(status_code=404, detail="Bug not found")
    
    db.delete(db_bug)
    db.commit()
    return {"message": "Bug deleted"}
