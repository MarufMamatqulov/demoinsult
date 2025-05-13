import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './FormMedical.css';
import AIRecommendations from './AIRecommendations.tsx';

export default function Phq9Form() {
  const { t } = useTranslation();
  const [answers, setAnswers] = useState({ q1: 0, q2: 0, q3: 0, q4: 0, q5: 0, q6: 0, q7: 0, q8: 0, q9: 0 });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

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
      const response = await fetch('/api/phq9/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(answers)
      });
      const data = await response.json();
      setResult(data.result);
    } catch (err) {
      setResult('Error analyzing PHQ-9.');
    }
    setLoading(false);
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
