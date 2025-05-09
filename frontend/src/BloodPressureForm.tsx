import React, { useState } from 'react';
import './FormMedical.css';

const BloodPressureForm = () => {
  const [systolic, setSystolic] = useState('');
  const [diastolic, setDiastolic] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult('');
    try {
      const response = await fetch('/api/blood-pressure/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ systolic, diastolic })
      });
      const data = await response.json();
      setResult(data.result);
    } catch (err) {
      setResult('Error analyzing blood pressure.');
    }
    setLoading(false);
  };

  return (
    <div className="medical-form-container animate-fade-in">
      <h2 className="form-title">Blood Pressure Monitoring</h2>
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
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>
      {result && (
        <div className="form-result animate-pop-in">
          <h3>Result</h3>
          <p>{result}</p>
        </div>
      )}
    </div>
  );
};

export default BloodPressureForm;
