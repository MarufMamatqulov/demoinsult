import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './FormMedical.css';
import AIRecommendations from './AIRecommendations.tsx';

export default function BloodPressureForm() {
  const { t } = useTranslation();
  const [systolic, setSystolic] = useState('');
  const [diastolic, setDiastolic] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult('');
    try {
      const response = await fetch('http://localhost:8000/bp/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ systolic, diastolic })
      });
      const data = await response.json();
      setResult(data.message);
    } catch (err) {
      setResult('Error analyzing blood pressure.');
    }
    setLoading(false);
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
