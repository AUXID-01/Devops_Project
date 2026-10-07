import React, { useState, useEffect } from 'react';
import { X, Search, Terminal } from 'lucide-react';
import axios from 'axios';

export default function BugModal({ bug, project_id, onClose, onSaved }) {
  const isEditing = !!bug;
  
  const [title, setTitle] = useState(bug?.title || '');
  const [description, setDescription] = useState(bug?.description || '');
  const [severity, setSeverity] = useState(bug?.severity || 'MEDIUM');
  const [status, setStatus] = useState(bug?.status || 'OPEN');
  const [affectedFile, setAffectedFile] = useState(bug?.affected_file || '');
  const [lineNumber, setLineNumber] = useState(bug?.line_number || '');
  
  const [analysis, setAnalysis] = useState(null);
  const [analysisError, setAnalysisError] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isLoadingAnalysis, setIsLoadingAnalysis] = useState(isEditing);

  useEffect(() => {
    if (isEditing && bug.id) {
      loadAnalysis();
    } else {
      setIsLoadingAnalysis(false);
    }
  }, [bug]);

  const loadAnalysis = async () => {
    try {
      setIsLoadingAnalysis(true);
      const res = await axios.get(`/api/bugs/${bug.id}/analysis`);
      setAnalysis(res.data);
      setAnalysisError(null);
    } catch (err) {
      setAnalysis(null);
    } finally {
      setIsLoadingAnalysis(false);
    }
  };

  const handleRunAnalysis = async () => {
    try {
      setIsAnalyzing(true);
      setAnalysisError(null);
      const res = await axios.post(`/api/bugs/${bug.id}/analyze`);
      setAnalysis(res.data);
    } catch (err) {
      console.error(err);
      if (err.response && err.response.data && err.response.data.detail) {
        setAnalysisError(`Analysis Failed: ${err.response.data.detail}`);
      } else {
        setAnalysisError("An unexpected error occurred while analyzing the bug.");
      }
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const payload = {
      title,
      description,
      severity,
      status,
      affected_file: affectedFile,
      line_number: lineNumber ? parseInt(lineNumber, 10) : null
    };

    try {
      if (isEditing) {
        await axios.put(`/api/bugs/${bug.id}`, payload);
      } else {
        await axios.post(`/api/projects/${project_id}/bugs`, payload);
      }
      onSaved();
    } catch (err) {
      alert("Failed to save bug");
      console.error(err);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2 style={{ margin: 0 }}>{isEditing ? 'Bug Details' : 'Report New Bug'}</h2>
          <button className="btn" onClick={onClose} style={{ padding: '0.25rem' }}><X size={24} /></button>
        </div>
        
        <div className="modal-body">
          <form id="bug-form" onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Title</label>
              <input type="text" className="form-input" value={title} onChange={e => setTitle(e.target.value)} required />
            </div>
            
            <div className="grid grid-cols-2">
              <div className="form-group">
                <label className="form-label">Severity</label>
                <select className="form-select" value={severity} onChange={e => setSeverity(e.target.value)}>
                  <option value="LOW">Low</option>
                  <option value="MEDIUM">Medium</option>
                  <option value="HIGH">High</option>
                  <option value="CRITICAL">Critical</option>
                </select>
              </div>
              <div className="form-group">
                <label className="form-label">Status</label>
                <select className="form-select" value={status} onChange={e => setStatus(e.target.value)}>
                  <option value="OPEN">Open</option>
                  <option value="IN_PROGRESS">In Progress</option>
                  <option value="RESOLVED">Resolved</option>
                  <option value="CLOSED">Closed</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label className="form-label">Description</label>
              <textarea className="form-textarea" rows="3" value={description} onChange={e => setDescription(e.target.value)} required></textarea>
            </div>

            <div className="grid grid-cols-2">
              <div className="form-group">
                <label className="form-label">Affected File</label>
                <input type="text" className="form-input" value={affectedFile} onChange={e => setAffectedFile(e.target.value)} placeholder="e.g. app/models.py" required />
              </div>
              <div className="form-group">
                <label className="form-label">Line Number (Optional)</label>
                <input type="number" className="form-input" value={lineNumber} onChange={e => setLineNumber(e.target.value)} placeholder="e.g. 42" />
              </div>
            </div>
          </form>

          {isEditing && (
            <div className="mt-8 border-t pt-4" style={{ borderColor: 'var(--border-color)' }}>
              <div className="flex justify-between items-center mb-4">
                <h3 className="flex items-center gap-2 m-0"><Search size={20} /> Automated Analysis</h3>
                <button 
                  className="btn btn-primary" 
                  onClick={handleRunAnalysis} 
                  disabled={isAnalyzing}
                >
                  <Terminal size={16} /> {isAnalyzing ? 'Analyzing...' : 'Run Analysis'}
                </button>
              </div>
              {analysisError && (
                <div className="mb-4 p-3 bg-red-900 border border-red-700 text-red-200 rounded" style={{ backgroundColor: 'rgba(255, 76, 76, 0.1)', borderColor: '#ff4c4c', color: '#ff4c4c' }}>
                  <strong>Error:</strong> {analysisError}
                </div>
              )}
              
              {isLoadingAnalysis ? (
                <p className="text-muted text-center py-4">Loading analysis...</p>
              ) : analysis ? (
                <div className="card bg-dark">
                  {analysis.detected_snippet && (
                    <div className="mb-4">
                      <h4 className="text-sm text-muted">Detected Snippet</h4>
                      <div className="code-block">{analysis.detected_snippet}</div>
                    </div>
                  )}
                  <div className="mb-4">
                    <h4 className="text-sm text-muted">Potential Cause</h4>
                    <p>{analysis.potential_cause}</p>
                  </div>
                  {analysis.suggested_fix && (
                    <div className="mb-4">
                      <h4 className="text-sm text-muted">Suggested Fix</h4>
                      <p>{analysis.suggested_fix}</p>
                    </div>
                  )}
                  <div>
                    <h4 className="text-sm text-muted">Reproduction Steps</h4>
                    <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>{analysis.reproduction_steps}</pre>
                  </div>
                </div>
              ) : !analysisError ? (
                <div className="text-center text-muted py-4 border rounded" style={{ borderColor: 'var(--border-color)' }}>
                  <p>No analysis run yet. Click 'Run Analysis' to let BugBoard analyze this bug.</p>
                </div>
              ) : null}
            </div>
          )}
        </div>
        
        <div className="modal-footer">
          <button className="btn btn-danger" onClick={onClose}>Cancel</button>
          <button type="submit" form="bug-form" className="btn btn-primary">
            {isEditing ? 'Save Changes' : 'Report Bug'}
          </button>
        </div>
      </div>
    </div>
  );
}
