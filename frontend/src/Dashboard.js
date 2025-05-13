import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './Dashboard.css';

const Dashboard = () => {
  const { t } = useTranslation();

  return (
    <div className="dashboard-container">
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
