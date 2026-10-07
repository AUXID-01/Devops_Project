import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Navbar from './components/Navbar';
import ProjectUpload from './components/ProjectUpload';
import ProjectList from './components/ProjectList';
import BugList from './components/BugList';
import BugModal from './components/BugModal';
import { Plus } from 'lucide-react';

export default function App() {
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(null);
  const [bugs, setBugs] = useState([]);
  
  const [isBugModalOpen, setIsBugModalOpen] = useState(false);
  const [selectedBug, setSelectedBug] = useState(null);

  useEffect(() => {
    fetchProjects();
  }, []);

  useEffect(() => {
    if (selectedProjectId) {
      fetchBugs(selectedProjectId);
    } else {
      setBugs([]);
    }
  }, [selectedProjectId]);

  const fetchProjects = async () => {
    try {
      const res = await axios.get('/api/projects');
      setProjects(res.data);
    } catch (err) {
      console.error("Failed to fetch projects", err);
    }
  };

  const fetchBugs = async (projectId) => {
    try {
      const res = await axios.get(`/api/projects/${projectId}/bugs`);
      setBugs(res.data);
    } catch (err) {
      console.error("Failed to fetch bugs", err);
    }
  };

  const handleUploadProject = async (name, file) => {
    const formData = new FormData();
    formData.append('name', name);
    formData.append('file', file);
    
    await axios.post('/api/projects', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    fetchProjects();
  };

  const handleDeleteProject = async (id) => {
    if (confirm("Are you sure you want to delete this project?")) {
      await axios.delete(`/api/projects/${id}`);
      if (selectedProjectId === id) setSelectedProjectId(null);
      fetchProjects();
    }
  };

  const handleDeleteBug = async (id) => {
    if (confirm("Are you sure you want to delete this bug?")) {
      await axios.delete(`/api/bugs/${id}`);
      fetchBugs(selectedProjectId);
    }
  };

  const openNewBugModal = () => {
    setSelectedBug(null);
    setIsBugModalOpen(true);
  };

  const openEditBugModal = (bug) => {
    setSelectedBug(bug);
    setIsBugModalOpen(true);
  };

  const handleBugSaved = () => {
    setIsBugModalOpen(false);
    fetchBugs(selectedProjectId);
  };

  const allBugsCount = bugs.length; // Simplified for MVP, ideally calculate across all projects or backend API
  const criticalCount = bugs.filter(b => b.severity === 'HIGH' || b.severity === 'CRITICAL').length;

  return (
    <div className="app-container">
      <Navbar 
        projectsCount={projects.length} 
        bugsCount={allBugsCount} 
        criticalCount={criticalCount} 
      />
      
      <main className="main-content container">
        <ProjectUpload onUpload={handleUploadProject} />
        
        <div className="mb-8 border-b pb-4" style={{ borderColor: 'var(--border-color)' }}>
          <h2 className="mb-4">Your Projects</h2>
          <ProjectList 
            projects={projects} 
            selectedProjectId={selectedProjectId}
            onSelect={setSelectedProjectId}
            onDelete={handleDeleteProject}
          />
        </div>

        {selectedProjectId && (
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2>Project Bugs</h2>
              <button className="btn btn-primary" onClick={openNewBugModal}>
                <Plus size={16} /> Report Bug
              </button>
            </div>
            <BugList 
              bugs={bugs} 
              onSelectBug={openEditBugModal}
              onDeleteBug={handleDeleteBug}
            />
          </div>
        )}
      </main>

      {isBugModalOpen && (
        <BugModal 
          bug={selectedBug} 
          project_id={selectedProjectId}
          onClose={() => setIsBugModalOpen(false)}
          onSaved={handleBugSaved}
        />
      )}
    </div>
  );
}
