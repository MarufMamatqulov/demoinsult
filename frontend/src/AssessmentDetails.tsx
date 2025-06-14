import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { useAuth } from './context/AuthContext';
import './styles/AssessmentDetails.css';

const AssessmentDetails = () => {
  const { t } = useTranslation();
  const { id } = useParams();
  const navigate = useNavigate();
  const { token, isAuthenticated } = useAuth();
  const [assessment, setAssessment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // API URL from environment variable
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const fetchAssessmentDetails = async () => {
      if (!isAuthenticated || !id) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const response = await axios.get(`${API_URL}/assessments/${id}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        setAssessment(response.data);
      } catch (err) {
        console.error('Failed to fetch assessment details:', err);
        setError('Failed to load assessment details. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchAssessmentDetails();
  }, [isAuthenticated, token, id, API_URL]);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    }).format(date);
  };

  const handleDeleteAssessment = async () => {
    if (!window.confirm('Are you sure you want to delete this assessment? This action cannot be undone.')) {
      return;
    }

    try {
      await axios.delete(`${API_URL}/assessments/${id}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      navigate('/assessment-history');
    } catch (err) {
      console.error('Failed to delete assessment:', err);
      setError('Failed to delete the assessment. Please try again later.');
    }
  };

  const renderAssessmentTypeTitle = (type) => {
    switch (type) {
      case 'blood_pressure':
        return 'Blood Pressure Assessment';
      case 'phq9':
        return 'PHQ-9 Depression Screening';
      case 'nihss':
        return 'NIH Stroke Scale Assessment';
      case 'speech_hearing':
        return 'Speech & Hearing Assessment';
      case 'movement':
        return 'Movement Assessment';
      default:
        return type ? type.replace('_', ' ').charAt(0).toUpperCase() + type.slice(1) : 'Assessment';
    }
  };

  const renderDataFields = () => {
    if (!assessment || !assessment.data) return null;

    return Object.entries(assessment.data).map(([key, value]) => {
      // Skip rendering recommendations field here
      if (key === 'recommendations') return null;

      // Format the key for display
      const formattedKey = key
        .replace(/_/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');

      return (
        <div key={key} className="assessment-detail-item">
          <div className="assessment-detail-label">{formattedKey}</div>
          <div className="assessment-detail-value">
            {typeof value === 'object' ? JSON.stringify(value, null, 2) : value.toString()}
          </div>
        </div>
      );
    });
  };

  if (loading) {
    return <div className="assessment-details-loading">Loading assessment details...</div>;
  }

  if (error) {
    return <div className="assessment-details-error">{error}</div>;
  }

  if (!isAuthenticated) {
    return <div className="assessment-details-unauthorized">Please log in to view assessment details.</div>;
  }

  if (!assessment) {
    return <div className="assessment-details-not-found">Assessment not found.</div>;
  }

  return (
    <div className="assessment-details-container">
      <div className="assessment-details-header">
        <h1>{renderAssessmentTypeTitle(assessment.type)}</h1>
        <div className="assessment-details-date">
          Conducted on {formatDate(assessment.created_at)}
        </div>
      </div>

      <div className="assessment-details-content">
        <div className="assessment-details-section">
          <h2>Results</h2>
          <div className="assessment-details-data">
            {renderDataFields()}
          </div>
        </div>

        {assessment.data.recommendations && (
          <div className="assessment-details-section recommendations-section">
            <h2>Recommendations</h2>
            <div className="assessment-recommendations">
              {assessment.data.recommendations}
            </div>
          </div>
        )}
      </div>

      <div className="assessment-details-actions">
        <button 
          className="back-button" 
          onClick={() => navigate('/assessment-history')}
        >
          Back to History
        </button>
        <button 
          className="delete-button" 
          onClick={handleDeleteAssessment}
        >
          Delete This Record
        </button>
      </div>
    </div>
  );
};

export default AssessmentDetails;
