import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useAuth } from './context/AuthContext';
import axios from 'axios';
import './FormMedical.css';
import AIRecommendations from './AIRecommendations';

export default function NihssForm() {
  const { t } = useTranslation();
  const { token, isAuthenticated } = useAuth();
  const [formData, setFormData] = useState({
    nihs_1: '', nihs_2: '', nihs_3: '', nihs_4: '', nihs_5: '',
    nihs_6: '', nihs_7: '', nihs_8: '', nihs_9: '', nihs_10: '', nihs_11: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // API URL from environment variable
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const questions = [
    { label: t('nihss.q1'), max: 3, example: t('nihss.q1_example') },
    { label: t('nihss.q2'), max: 2, example: t('nihss.q2_example') },
    { label: t('nihss.q3'), max: 3, example: t('nihss.q3_example') },
    { label: t('nihss.q4'), max: 3, example: t('nihss.q4_example') },
    { label: t('nihss.q5'), max: 4, example: t('nihss.q5_example') },
    { label: t('nihss.q6'), max: 4, example: t('nihss.q6_example') },
    { label: t('nihss.q7'), max: 2, example: t('nihss.q7_example') },
    { label: t('nihss.q8'), max: 2, example: t('nihss.q8_example') },
    { label: t('nihss.q9'), max: 3, example: t('nihss.q9_example') },
    { label: t('nihss.q10'), max: 2, example: t('nihss.q10_example') },
    { label: t('nihss.q11'), max: 2, example: t('nihss.q11_example') }
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
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
      
      const response = await fetch('/nihss/analyze', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      setResult(data.severity);
      
      // Calculate total score
      const totalScore = Object.values(formData).reduce((sum, val) => sum + (parseInt(val) || 0), 0);
      
      // If user is authenticated, save the assessment to their history
      if (isAuthenticated && token) {
        try {
          await axios.post(`${API_URL}/assessments`, {
            type: 'nihss',
            data: {
              answers: formData,
              total_score: totalScore,
              severity: data.severity,
              recommendations: data.recommendations || ''
            }
          }, { headers });
          console.log('NIHSS assessment saved to user history');
        } catch (historyErr) {
          console.error('Failed to save NIHSS assessment to history:', historyErr);
        }
      }
    } catch (err) {
      setResult('Xatolik yuz berdi. NIHSS tahlil qilinmadi.');
    }
    setLoading(false);
  };

  return (
    <div className="medical-form-container animate-fade-in">
      <h2 className="form-title">{t('nihss.title')}</h2>
      <p className="form-description">
        {t('nihss.description')}
      </p>
      <form className="medical-form" onSubmit={handleSubmit}>
        {questions.map((question, idx) => (
          <div className="form-group" key={idx}>
            <label className="form-label">{question.label} (Max: {question.max})</label>
            <input
              className="form-input"
              type="number"
              name={`nihs_${idx + 1}`}
              value={formData[`nihs_${idx + 1}`]}
              onChange={handleChange}
              min="0"
              max={question.max}
              required
            />
            <small className="form-note">Masalan: {question.example}</small>
          </div>
        ))}
        <button className="form-submit-btn" type="submit" disabled={loading}>
          {loading ? 'Tahlil qilinmoqda...' : 'Yuborish'}
        </button>
      </form>      {result && (
        <div className="result-container">
          <h3>Natija</h3>
          <p>{result}</p>
          
          {/* Add AI Recommendations component */}
          <AIRecommendations 
            assessmentType="nihss" 
            assessmentData={formData} 
            language={localStorage.getItem('i18nextLng')?.split('-')[0] || 'en'}
          />
        </div>
      )}
    </div>
  );
}
