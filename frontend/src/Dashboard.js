import React from 'react';
import { Link } from 'react-router-dom';
import './Dashboard.css';

function Dashboard() {
  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Stroke Rehabilitation AI Platform</h1>
        <p className="dashboard-subtitle">Empowering Recovery with AI-Driven Insights</p>
      </header>
      <nav className="dashboard-nav">
        <ul>
          <li><Link to="/phq9" className="dashboard-link">PHQ-9 Analysis</Link></li>
          <li><Link to="/blood-pressure" className="dashboard-link">Blood Pressure Monitoring</Link></li>
          <li><Link to="/exercise" className="dashboard-link">Exercise Tracking</Link></li>
          <li><Link to="/audio-upload" className="dashboard-link">Audio Upload</Link></li>
          <li><Link to="/video-upload" className="dashboard-link">Video Upload</Link></li>
          <li><Link to="/history" className="dashboard-link">History and Trends</Link></li>
        </ul>
      </nav>
      <footer className="dashboard-footer">
        <p>&copy; {new Date().getFullYear()} Stroke Rehabilitation AI Platform</p>
      </footer>
    </div>
  );
}

export default Dashboard;
