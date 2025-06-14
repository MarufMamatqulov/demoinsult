import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from './context/AuthContext';
import axios from 'axios';
import './FormMedical.css';
import AIRecommendations from './AIRecommendations';
import { endpoints } from './config/api';

export default function Phq9Form() {
  const { t } = useTranslation();
  const { token, isAuthenticated } = useAuth();
  const [answers, setAnswers] = useState({ q1: 0, q2: 0, q3: 0, q4: 0, q5: 0, q6: 0, q7: 0, q8: 0, q9: 0 });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const questions = [
    t('phq9.q1'),
    t('phq9.q2'),
    t('phq9.q3'),
    t('phq9.q4'),
    t('phq9.q5'),
    t('phq9.q6'),
    t('phq9.q7'),
    t('phq9.q8'),
    t('phq9.q9')
  ];

  const options = [
    t('phq9.opt1'),
    t('phq9.opt2'),
    t('phq9.opt3'),
    t('phq9.opt4')
  ];

  const handleChange = (q, value) => {
    setAnswers({ ...answers, [q]: value });
  };  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      // Set up headers with auth token if user is authenticated
      const headers = {
        'Content-Type': 'application/json'
      };
      
      if (isAuthenticated && token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
      
      const response = await fetch(endpoints.phqAnalyze, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(answers)
      });
      
      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (data.status === "error") {
        throw new Error(data.message || "Unknown error occurred");
      }
      
      setResult(`Depression level: ${data.depression_level}, Total score: ${data.total_score}`);
      
      // If user is authenticated, save the assessment to their history
      if (isAuthenticated && token) {
        try {
          await axios.post(`${API_URL}/assessments`, {
            type: 'phq9',
            data: {
              answers: answers,
              score: data.total_score,
              severity: data.depression_level,
              recommendations: data.recommendations || ''
            }
          }, { headers });
          console.log('PHQ-9 assessment saved to user history');
        } catch (historyErr) {
          console.error('Failed to save PHQ-9 assessment to history:', historyErr);
        }
      }
    } catch (err) {
      console.error("PHQ-9 analysis error:", err);
      setResult(`Error analyzing PHQ-9: ${err.message || "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="medical-form-container animate-fade-in">
      <h2 className="form-title">{t('phq9.title')}</h2>
      <p className="form-description">
        {t('phq9.description')}
      </p>
      <form className="medical-form" onSubmit={handleSubmit}>
        {questions.map((question, idx) => (
          <div className="form-group" key={idx}>
            <label className="form-label">{question}</label>
            <select
              className="form-input"
              value={answers[`q${idx + 1}`]}
              onChange={(e) => handleChange(`q${idx + 1}`, parseInt(e.target.value))}
              required
            >
              {options.map((option, value) => (
                <option key={value} value={value}>{option}</option>
              ))}
            </select>
          </div>
        ))}
        <button className="form-submit-btn" type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Submit'}
        </button>
      </form>      {result && (
        <div className="result-container">
          <h3>Result</h3>
          <p>{result}</p>
          
          {/* Add AI Recommendations component */}
          <AIRecommendations 
            assessmentType="phq9" 
            assessmentData={answers} 
            language={localStorage.getItem('i18nextLng')?.split('-')[0] || 'en'}
          />
        </div>
      )}
    </div>
  );
}
