import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { useAuth } from './context/AuthContext';
import './styles/AssessmentHistory.css';

const AssessmentHistory = () => {
  const { t } = useTranslation();
  const { token, isAuthenticated } = useAuth();
  const [assessments, setAssessments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');

  // API URL from environment variable
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const fetchAssessments = async () => {
      if (!isAuthenticated) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const response = await axios.get(`${API_URL}/assessments/history`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setAssessments(response.data);
      } catch (err) {
        console.error('Failed to fetch assessment history:', err);
        setError('Failed to load your assessment history. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchAssessments();
  }, [isAuthenticated, token, API_URL]);

  const filteredAssessments = filter === 'all' 
    ? assessments 
    : assessments.filter(assessment => assessment.type === filter);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  const renderAssessmentDetails = (assessment) => {
    switch (assessment.type) {
      case 'blood_pressure':
        return (
          <>
            <div className="assessment-data-item">
              <span>Systolic:</span> {assessment.data.systolic} mmHg
            </div>
            <div className="assessment-data-item">
              <span>Diastolic:</span> {assessment.data.diastolic} mmHg
            </div>
            <div className="assessment-data-item">
              <span>Classification:</span> {assessment.data.classification}
            </div>
          </>
        );
      case 'phq9':
        return (
          <>
            <div className="assessment-data-item">
              <span>Score:</span> {assessment.data.score}
            </div>
            <div className="assessment-data-item">
              <span>Depression Severity:</span> {assessment.data.severity}
            </div>
          </>
        );
      case 'nihss':
        return (
          <>
            <div className="assessment-data-item">
              <span>Total Score:</span> {assessment.data.total_score}
            </div>
            <div className="assessment-data-item">
              <span>Stroke Severity:</span> {assessment.data.severity}
            </div>
          </>
        );
      case 'speech_hearing':
        return (
          <>
            <div className="assessment-data-item">
              <span>Speech Analysis:</span> {assessment.data.speech_analysis}
            </div>
            <div className="assessment-data-item">
              <span>Hearing Status:</span> {assessment.data.hearing_status}
            </div>
          </>
        );
      case 'movement':
        return (
          <>
            <div className="assessment-data-item">
              <span>Movement Score:</span> {assessment.data.score}
            </div>
            <div className="assessment-data-item">
              <span>Affected Side:</span> {assessment.data.affected_side}
            </div>
          </>
        );
      default:
        return <div>No detailed information available</div>;
    }
  };

  if (loading) {
    return <div className="assessment-history-loading">Loading your assessment history...</div>;
  }

  if (error) {
    return <div className="assessment-history-error">{error}</div>;
  }

  if (!isAuthenticated) {
    return <div className="assessment-history-unauthorized">Please log in to view your assessment history.</div>;
  }

  return (
    <div className="assessment-history-container">
      <h1>Your Assessment History</h1>
      
      <div className="assessment-filter">
        <label htmlFor="assessment-type-filter">Filter by type:</label>
        <select 
          id="assessment-type-filter" 
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        >
          <option value="all">All Assessments</option>
          <option value="blood_pressure">Blood Pressure</option>
          <option value="phq9">PHQ-9</option>
          <option value="nihss">NIHSS</option>
          <option value="speech_hearing">Speech & Hearing</option>
          <option value="movement">Movement</option>
        </select>
      </div>

      {filteredAssessments.length === 0 ? (
        <div className="no-assessments">
          {filter === 'all' 
            ? 'You have no assessment records yet. Complete an assessment to see your history.' 
            : `You have no ${filter} assessment records yet.`}
        </div>
      ) : (
        <div className="assessment-cards">
          {filteredAssessments.map((assessment, index) => (
            <div key={index} className="assessment-card">
              <div className="assessment-header">
                <h3>{assessment.type_display || assessment.type}</h3>
                <span className="assessment-date">{formatDate(assessment.created_at)}</span>
              </div>
              <div className="assessment-body">
                {renderAssessmentDetails(assessment)}
              </div>
              <div className="assessment-footer">
                <button 
                  className="view-details-button"
                  onClick={() => window.location.href = `/assessment-details/${assessment.id}`}
                >
                  View Full Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AssessmentHistory;
