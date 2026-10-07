import React from 'react';
import { FileWarning, Clock, Trash2, Edit } from 'lucide-react';

export default function BugList({ bugs, onSelectBug, onDeleteBug }) {
  if (bugs.length === 0) {
    return (
      <div className="card text-center text-muted py-8">
        <FileWarning size={48} style={{ margin: '0 auto 1rem', opacity: 0.5 }} />
        <p>No bugs reported for this project.</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 gap-4">
      {bugs.map((bug) => (
        <div 
          key={bug.id} 
          className="card flex justify-between items-center" 
          style={{ cursor: 'pointer', padding: '1rem' }}
          onClick={() => onSelectBug(bug)}
        >
          <div>
            <div className="flex items-center gap-2 mb-1">
              <h4 style={{ margin: 0 }}>{bug.title}</h4>
              <span className={`badge badge-${bug.severity.toLowerCase()}`}>{bug.severity}</span>
              <span className={`badge badge-${bug.status.toLowerCase()}`}>{bug.status.replace('_', ' ')}</span>
            </div>
            <div className="text-sm text-muted flex items-center gap-2">
              <span className="flex items-center gap-1">
                <FileWarning size={14} /> {bug.affected_file}{bug.line_number ? `:${bug.line_number}` : ''}
              </span>
              <span className="flex items-center gap-1">
                <Clock size={14} /> {new Date(bug.created_at).toLocaleDateString()}
              </span>
            </div>
          </div>
          
          <div className="flex gap-2">
            <button 
              className="btn btn-primary" 
              onClick={(e) => { e.stopPropagation(); onSelectBug(bug); }}
            >
              <Edit size={16} /> Details
            </button>
            <button 
              className="btn btn-danger" 
              onClick={(e) => { e.stopPropagation(); onDeleteBug(bug.id); }}
            >
              <Trash2 size={16} />
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
