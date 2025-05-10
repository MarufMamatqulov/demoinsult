import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import './FormMedical.css';

export default function BPTrendForm() {
  const { t } = useTranslation();
  const [measurements, setMeasurements] = useState([
    { systolic: '', diastolic: '' },
    { systolic: '', diastolic: '' },
    { systolic: '', diastolic: '' }
  ]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (idx, field, value) => {
    const updated = measurements.map((m, i) =>
      i === idx ? { ...m, [field]: value } : m
    );
    setMeasurements(updated);
  };

  const handleAdd = () => {
    setMeasurements([...measurements, { systolic: '', diastolic: '' }]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch('/bp/trend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ measurements: measurements.map(m => ({ systolic: Number(m.systolic), diastolic: Number(m.diastolic) })) })
      });
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setResult({ status: 'Error', warning: 'Could not analyze trend.' });
    }
    setLoading(false);
  };

  return (
    <div className="medical-form-container animate-fade-in">
      <h2 className="form-title">{t('bpTrend.title')}</h2>
      <p className="form-description">{t('bpTrend.description')}</p>
      <form className="medical-form" onSubmit={handleSubmit}>
        {measurements.map((m, idx) => (
          <div className="form-group" key={idx}>
            <label className="form-label">Day {idx + 1}</label>
            <div style={{ display: 'flex', gap: '1rem' }}>
              <input
                className="form-input"
                type="number"
                placeholder="Systolic"
                value={m.systolic}
                onChange={e => handleChange(idx, 'systolic', e.target.value)}
                required
              />
              <input
                className="form-input"
                type="number"
                placeholder="Diastolic"
                value={m.diastolic}
                onChange={e => handleChange(idx, 'diastolic', e.target.value)}
                required
              />
            </div>
          </div>
        ))}
        <button type="button" className="form-add-btn" onClick={handleAdd}>Add Day</button>
        <button className="form-submit-btn" type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Submit'}
        </button>
      </form>
      {result && (
        <div className="result-container">
          <h3>Result</h3>
          <p>Status: {result.status}</p>
          <p>Warning: {result.warning}</p>
        </div>
      )}
    </div>
  );
}
