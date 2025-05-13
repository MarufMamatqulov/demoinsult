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
      // First, validate inputs
      const systolicNum = parseInt(systolic);
      const diastolicNum = parseInt(diastolic);
      
      if (isNaN(systolicNum) || isNaN(diastolicNum) || systolicNum <= 0 || diastolicNum <= 0) {
        throw new Error("Please enter valid blood pressure values");
      }
      
      const response = await fetch('http://localhost:8000/bp/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          systolic: systolicNum, 
          diastolic: diastolicNum 
        })
      });
      
      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Set result even if message is undefined
      setResult(data.message || 'Blood pressure analysis complete.');
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
