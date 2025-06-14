import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useAuth } from './context/AuthContext';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = () => {
  const { t } = useTranslation();
  const { user, isAuthenticated, token } = useAuth();
  const [recentAssessments, setRecentAssessments] = useState([]);
  const [loading, setLoading] = useState(false);

  // API URL from environment variable
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    // Fetch recent assessments if user is authenticated
    const fetchRecentAssessments = async () => {
      if (!isAuthenticated || !token) return;
      
      try {
        setLoading(true);
        const response = await axios.get(`${API_URL}/assessments/history?limit=3`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setRecentAssessments(response.data);
      } catch (err) {
        console.error('Failed to fetch recent assessments:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchRecentAssessments();
  }, [isAuthenticated, token, API_URL]);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  const getAssessmentTypeDisplay = (type) => {
    switch (type) {
      case 'blood_pressure': return 'Blood Pressure';
      case 'phq9': return 'PHQ-9 Depression';
      case 'nihss': return 'NIH Stroke Scale';
      case 'speech_hearing': return 'Speech & Hearing';
      case 'movement': return 'Movement';
      default: return type ? type.replace('_', ' ') : 'Assessment';
    }
  };

  return (
    <div className="dashboard-container">
      {isAuthenticated && user && (
        <div className="user-welcome-section">
          <h2>Welcome, {user.first_name || user.email}</h2>
          <p>Track your stroke rehabilitation progress and access personalized health tools</p>
          
          <div className="quick-links">
            <Link to="/profile" className="quick-link">My Profile</Link>
            <Link to="/assessment-history" className="quick-link">My Assessment History</Link>
            <Link to="/rehabilitation" className="quick-link">My Rehabilitation Plan</Link>
          </div>
          
          {recentAssessments.length > 0 && (
            <div className="recent-assessments">
              <h3>Recent Assessments</h3>
              <div className="recent-assessments-list">
                {recentAssessments.map((assessment, index) => (
                  <Link 
                    key={index} 
                    to={`/assessment-details/${assessment.id}`}
                    className="recent-assessment-item"
                  >
                    <div className="assessment-type">
                      {getAssessmentTypeDisplay(assessment.type)}
                    </div>
                    <div className="assessment-date">
                      {formatDate(assessment.created_at)}
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      <h1 className="dashboard-title">{t('dashboard.title')}</h1>
      <div className="dashboard-grid">
        <div className="dashboard-card special-highlight-card">
          <h2>Stroke Rehabilitation</h2>
          <p>Access rehabilitation tools, exercises, and resources</p>
          <div className="card-links">
            <Link to="/rehabilitation" className="dashboard-link">
              <span className="card-icon">🔄</span>
              {t('dashboard.rehabilitation', 'Rehabilitation Analysis & Exercises')}
            </Link>
          </div>
        </div>
        
        <div className="dashboard-card">
          <h2>Stroke Assessment</h2>
          <p>Evaluate stroke symptoms and severity</p>
          <div className="card-links">
            <Link to="/nihss" className="dashboard-link">
              <span className="card-icon">🧠</span>
              {t('dashboard.nihss')}
            </Link>
          </div>
        </div>
        
        <div className="dashboard-card">
          <h2>Physical Assessment</h2>
          <p>Monitor vital signs and physical capabilities</p>
          <div className="card-links">
            <Link to="/blood-pressure" className="dashboard-link">
              <span className="card-icon">❤️</span>
              {t('dashboard.bloodPressure')}
            </Link>
            <Link to="/bp-trend" className="dashboard-link">
              <span className="card-icon">📈</span>
              {t('dashboard.bpTrend')}
            </Link>
          </div>
        </div>
        
        <div className="dashboard-card">
          <h2>Mental Health</h2>
          <p>Assess psychological well-being</p>
          <div className="card-links">
            <Link to="/phq9" className="dashboard-link">
              <span className="card-icon">🧠</span>
              {t('dashboard.phq9')}
            </Link>
          </div>
        </div>
        
        <div className="dashboard-card highlight-card">
          <h2>Communication Assessment</h2>
          <p>Evaluate speech and hearing abilities</p>
          <div className="card-links">
            <Link to="/speech-hearing-assessment" className="dashboard-link">
              <span className="card-icon">🗣️</span>
              {t('dashboard.speechHearing')}
            </Link>
          </div>
        </div>
        
        <div className="dashboard-card highlight-card">
          <h2>Movement Assessment</h2>
          <p>Evaluate motor function and mobility</p>
          <div className="card-links">
            <Link to="/movement-assessment" className="dashboard-link">
              <span className="card-icon">🚶</span>
              {t('dashboard.movement')}
            </Link>
          </div>
        </div>
          <div className="dashboard-card">
          <h2>Patient Records</h2>
          <p>View patient history and reports</p>
          <div className="card-links">
            <Link to="/history" className="dashboard-link">
              <span className="card-icon">📋</span>
              {t('dashboard.history')}
            </Link>
          </div>
        </div>
        
        <div className="dashboard-card special-highlight-card">
          <h2>AI Assistant</h2>
          <p>Chat with our AI assistant for personalized rehabilitation advice</p>
          <div className="card-links">
            <Link to="/patient-chat" className="dashboard-link">
              <span className="card-icon">💬</span>
              Rehabilitation AI Chat
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
