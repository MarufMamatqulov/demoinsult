import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from './context/AuthContext';
import axios from 'axios';
import './FormMedical.css';
import AIRecommendations from './AIRecommendations';

export default function BloodPressureForm() {
  const { t } = useTranslation();
  const { token, isAuthenticated } = useAuth();
  const [systolic, setSystolic] = useState('');
  const [diastolic, setDiastolic] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  
  // API URL from environment variable
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult('');
    try {
      // First, validate inputs
      const systolicNum = parseInt(systolic);
      const diastolicNum = parseInt(diastolic);
      
      if (isNaN(systolicNum) || isNaN(diastolicNum) || systolicNum <= 0 || diastolicNum <= 0) {
        throw new Error("Please enter valid blood pressure values");
      }
      
      // Set up headers with auth token if user is authenticated
      const headers = {
        'Content-Type': 'application/json'
      };
      
      if (isAuthenticated && token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      // Send the request
      const response = await axios.post(`${API_URL}/bp/analyze`, { 
        systolic: systolicNum, 
        diastolic: diastolicNum 
      }, { headers });
      
      // Set result
      setResult(response.data.message || 'Blood pressure analysis complete.');
      
      // If user is authenticated, also save the assessment to their history
      if (isAuthenticated && token) {
        try {
          await axios.post(`${API_URL}/assessments`, {
            type: 'blood_pressure',
            data: {
              systolic: systolicNum,
              diastolic: diastolicNum,
              classification: response.data.classification || 'Unknown',
              message: response.data.message || '',
              recommendations: response.data.recommendations || ''
            }
          }, { headers });
          console.log('Blood pressure assessment saved to user history');
        } catch (historyErr) {
          console.error('Failed to save assessment to history:', historyErr);
        }
      }
    } catch (err) {
      console.error("Blood pressure analysis error:", err);
      setResult(`Error analyzing blood pressure: ${err.message || 'Unknown error'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="medical-form-container animate-fade-in blood-pressure-form">
      <h2 className="form-title">{t('bloodPressure.title')}</h2>
      <p className="form-description">{t('bloodPressure.description')}</p>
      <form className="medical-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Systolic (mmHg)</label>
          <input
            className="form-input"
            type="number"
            min="50"
            max="250"
            value={systolic}
            onChange={(e) => setSystolic(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label className="form-label">Diastolic (mmHg)</label>
          <input
            className="form-input"
            type="number"
            min="30"
            max="150"
            value={diastolic}
            onChange={(e) => setDiastolic(e.target.value)}
            required
          />
        </div>
        <button className="form-submit-btn" type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Submit'}
        </button>
      </form>      {result && (
        <div className="result-container">
          <h3>Result</h3>
          <p>{result}</p>
          
          {/* Add AI Recommendations component */}
          <AIRecommendations 
            assessmentType="blood_pressure" 
            assessmentData={{ systolic, diastolic }} 
            language={localStorage.getItem('i18nextLng')?.split('-')[0] || 'en'}
          />
        </div>
      )}
    </div>
  );
}
