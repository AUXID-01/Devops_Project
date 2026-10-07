import React from 'react';
import { Folder, FileCode, Beaker, Trash2 } from 'lucide-react';

export default function ProjectList({ projects, onSelect, onDelete, selectedProjectId }) {
  if (projects.length === 0) {
    return (
      <div className="card text-center text-muted py-8">
        <Folder size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
        <p>No projects uploaded yet.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 mb-8">
      {projects.map((project) => (
        <div 
          key={project.id} 
          className="card" 
          style={{ 
            cursor: 'pointer',
            borderColor: selectedProjectId === project.id ? 'var(--accent-primary)' : 'var(--border-color)',
            borderWidth: selectedProjectId === project.id ? '2px' : '1px'
          }}
          onClick={() => onSelect(project.id)}
        >
          <div className="flex justify-between items-center mb-4">
            <h3 className="flex items-center gap-2">
              <Folder size={20} color="var(--accent-primary)" />
              {project.name}
            </h3>
            <button 
              className="btn btn-danger" 
              onClick={(e) => { e.stopPropagation(); onDelete(project.id); }}
              title="Delete Project"
            >
              <Trash2 size={16} />
            </button>
          </div>
          
          <div className="flex justify-between text-sm text-muted">
            <div className="flex items-center gap-1">
              <FileCode size={16} /> {project.python_file_count} Py
            </div>
            <div className="flex items-center gap-1">
              <Beaker size={16} /> {project.test_file_count} Tests
            </div>
            <div className="flex items-center gap-1">
              <Folder size={16} /> {project.file_count} Total
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
