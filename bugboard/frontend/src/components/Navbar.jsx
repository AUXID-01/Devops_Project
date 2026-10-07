import React from 'react';
import { Bug, Activity } from 'lucide-react';

export default function Navbar({ projectsCount, bugsCount, criticalCount }) {
  return (
    <header className="navbar">
      <div className="container navbar-container">
        <div className="navbar-brand">
          <Bug size={32} color="var(--accent-primary)" />
          <span>BugBoard</span>
        </div>
        <div className="navbar-stats">
          <div className="stat-item">
            <span className="stat-value">{projectsCount}</span>
            <span className="stat-label">Projects</span>
          </div>
          <div className="stat-item">
            <span className="stat-value">{bugsCount}</span>
            <span className="stat-label">Open Bugs</span>
          </div>
          <div className="stat-item">
            <span className="stat-value text-danger" style={{ color: 'var(--accent-danger)' }}>{criticalCount}</span>
            <span className="stat-label">High/Critical</span>
          </div>
          <div className="stat-item">
            <Activity size={24} color="var(--accent-success)" />
          </div>
        </div>
      </div>
    </header>
  );
}
