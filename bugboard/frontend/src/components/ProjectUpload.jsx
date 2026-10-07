import React, { useState, useRef } from 'react';
import { Upload, X } from 'lucide-react';

export default function ProjectUpload({ onUpload }) {
  const [name, setName] = useState('');
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.name.endsWith('.zip')) {
        setFile(droppedFile);
      } else {
        alert("Please upload a .zip file");
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name || !file) return;

    setIsUploading(true);
    try {
      await onUpload(name, file);
      setName('');
      setFile(null);
    } catch (err) {
      console.error(err);
      alert("Failed to upload project");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="card mb-8">
      <h2>Upload New Project</h2>
      <p className="text-muted mb-4">Upload a .zip file containing your Python project source code.</p>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Project Name</label>
          <input 
            type="text" 
            className="form-input" 
            value={name} 
            onChange={(e) => setName(e.target.value)} 
            placeholder="e.g. Authentication Service"
            required
          />
        </div>

        <div className="form-group">
          <label className="form-label">Project File (.zip)</label>
          {!file ? (
            <div 
              className="upload-zone"
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current.click()}
            >
              <Upload size={48} color="var(--text-muted)" style={{ margin: '0 auto 1rem' }} />
              <p>Click or drag and drop a .zip file here</p>
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileChange} 
                accept=".zip" 
                style={{ display: 'none' }} 
              />
            </div>
          ) : (
            <div className="flex items-center justify-between p-4 border rounded" style={{ borderColor: 'var(--border-color)', backgroundColor: 'rgba(30,41,59,0.5)' }}>
              <div className="flex items-center gap-2">
                <Upload size={24} color="var(--accent-primary)" />
                <span>{file.name}</span>
              </div>
              <button type="button" className="btn btn-danger" onClick={() => setFile(null)}>
                <X size={16} /> Remove
              </button>
            </div>
          )}
        </div>

        <button 
          type="submit" 
          className="btn btn-primary mt-4" 
          disabled={!name || !file || isUploading}
        >
          {isUploading ? 'Uploading & Analyzing...' : 'Upload Project'}
        </button>
      </form>
    </div>
  );
}
