from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models import SeverityLevel, BugStatus

class BugAnalysisBase(BaseModel):
    detected_snippet: Optional[str] = None
    potential_cause: str
    suggested_fix: Optional[str] = None
    reproduction_steps: str

class BugAnalysisCreate(BugAnalysisBase):
    pass

class BugAnalysisOut(BugAnalysisBase):
    id: int
    bug_id: int
    analyzed_at: datetime

    class Config:
        from_attributes = True

class BugBase(BaseModel):
    title: str
    description: str
    severity: SeverityLevel = SeverityLevel.MEDIUM
    status: BugStatus = BugStatus.OPEN
    affected_file: str
    line_number: Optional[int] = None

class BugCreate(BugBase):
    pass

class BugUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[SeverityLevel] = None
    status: Optional[BugStatus] = None

class BugOut(BugBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    name: str

class ProjectOut(ProjectBase):
    id: int
    filename: str
    file_count: int
    python_file_count: int
    test_file_count: int
    uploaded_at: datetime
    status: str
    
    class Config:
        from_attributes = True
