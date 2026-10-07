from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.database import Base

class SeverityLevel(str, enum.Enum):
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'
    CRITICAL = 'CRITICAL'

class BugStatus(str, enum.Enum):
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    RESOLVED = 'RESOLVED'
    CLOSED = 'CLOSED'

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    filename = Column(String(255), nullable=False)
    file_count = Column(Integer, default=0)
    python_file_count = Column(Integer, default=0)
    test_file_count = Column(Integer, default=0)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), default="PROCESSED")
    extracted_path = Column(String(500), nullable=False)

    bugs = relationship("Bug", cascade="all, delete-orphan", back_populates="project")

class Bug(Base):
    __tablename__ = "bugs"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(SQLEnum(SeverityLevel, name='severity_level'), default=SeverityLevel.MEDIUM)
    status = Column(SQLEnum(BugStatus, name='bug_status'), default=BugStatus.OPEN)
    affected_file = Column(String(255), nullable=False)
    line_number = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    project = relationship("Project", back_populates="bugs")
    analysis = relationship("BugAnalysis", uselist=False, cascade="all, delete-orphan", back_populates="bug")

class BugAnalysis(Base):
    __tablename__ = "bug_analyses"

    id = Column(Integer, primary_key=True, index=True)
    bug_id = Column(Integer, ForeignKey("bugs.id", ondelete="CASCADE"), unique=True, nullable=False)
    detected_snippet = Column(Text, nullable=True)
    potential_cause = Column(Text, nullable=False)
    suggested_fix = Column(Text, nullable=True)
    reproduction_steps = Column(Text, nullable=False)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())

    bug = relationship("Bug", back_populates="analysis")
