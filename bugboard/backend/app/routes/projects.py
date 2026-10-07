import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.config import settings
from app.analyzer import extract_and_analyze_project

router = APIRouter(prefix="/api/projects", tags=["projects"])

@router.post("", response_model=schemas.ProjectOut)
async def create_project(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed")

    # Create new project record
    db_project = models.Project(name=name, filename=file.filename, extracted_path="")
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    # Save uploaded zip
    upload_dir = settings.UPLOAD_DIR
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    zip_path = os.path.join(upload_dir, f"{db_project.id}_{file.filename}")
    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract and analyze
    extract_dir = os.path.join(upload_dir, str(db_project.id))
    try:
        stats = extract_and_analyze_project(zip_path, extract_dir)
        db_project.file_count = stats["file_count"]
        db_project.python_file_count = stats["python_file_count"]
        db_project.test_file_count = stats["test_file_count"]
        db_project.extracted_path = extract_dir
        db.commit()
        db.refresh(db_project)
    except Exception as e:
        # Cleanup on failure
        db.delete(db_project)
        db.commit()
        if os.path.exists(zip_path):
            os.remove(zip_path)
        if os.path.exists(extract_dir):
            shutil.rmtree(extract_dir)
        raise HTTPException(status_code=500, detail=f"Failed to process project: {str(e)}")

    # Clean up the zip file after extraction
    if os.path.exists(zip_path):
        os.remove(zip_path)

    return db_project

@router.get("", response_model=list[schemas.ProjectOut])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.extracted_path and os.path.exists(project.extracted_path):
        shutil.rmtree(project.extracted_path, ignore_errors=True)

    db.delete(project)
    db.commit()
    return {"message": "Project deleted"}
