"""initial schema

Revision ID: 0001
Revises: 
Create Date: 2026-10-07 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create enums manually if they don't exist
    op.execute("CREATE TYPE severity_level AS ENUM ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')")
    op.execute("CREATE TYPE bug_status AS ENUM ('OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED')")

    op.create_table('projects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('file_count', sa.Integer(), nullable=True),
    sa.Column('python_file_count', sa.Integer(), nullable=True),
    sa.Column('test_file_count', sa.Integer(), nullable=True),
    sa.Column('uploaded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('extracted_path', sa.String(length=500), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)
    
    op.create_table('bugs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('severity', postgresql.ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='severity_level', create_type=False), nullable=True),
    sa.Column('status', postgresql.ENUM('OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED', name='bug_status', create_type=False), nullable=True),
    sa.Column('affected_file', sa.String(length=255), nullable=False),
    sa.Column('line_number', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bugs_id'), 'bugs', ['id'], unique=False)
    
    op.create_table('bug_analyses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bug_id', sa.Integer(), nullable=False),
    sa.Column('detected_snippet', sa.Text(), nullable=True),
    sa.Column('potential_cause', sa.Text(), nullable=False),
    sa.Column('suggested_fix', sa.Text(), nullable=True),
    sa.Column('reproduction_steps', sa.Text(), nullable=False),
    sa.Column('analyzed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['bug_id'], ['bugs.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bug_id')
    )
    op.create_index(op.f('ix_bug_analyses_id'), 'bug_analyses', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_bug_analyses_id'), table_name='bug_analyses')
    op.drop_table('bug_analyses')
    op.drop_index(op.f('ix_bugs_id'), table_name='bugs')
    op.drop_table('bugs')
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')
    
    op.execute("DROP TYPE bug_status")
    op.execute("DROP TYPE severity_level")
