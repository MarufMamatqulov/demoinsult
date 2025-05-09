import React, { useState } from 'react';
import './FormMedical.css';

const Phq9Form = () => {
  const [answers, setAnswers] = useState({ q1: 0, q2: 0, q3: 0, q4: 0, q5: 0, q6: 0, q7: 0, q8: 0, q9: 0 });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const questions = [
    'Little interest or pleasure in doing things',
    'Feeling down, depressed, or hopeless',
    'Trouble falling or staying asleep, or sleeping too much',
    'Feeling tired or having little energy',
    'Poor appetite or overeating',
    'Feeling bad about yourself — or that you are a failure or have let yourself or your family down',
    'Trouble concentrating on things, such as reading the newspaper or watching television',
    'Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual',
    'Thoughts that you would be better off dead or of hurting yourself in some way'
  ];

  const options = [
    'Not at all',
    'Several days',
    'More than half the days',
    'Nearly every day'
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
      <h2 className="form-title">PHQ-9 Depression Assessment</h2>
      <form className="medical-form" onSubmit={handleSubmit}>
        {questions.map((q, idx) => (
          <div className="form-group" key={q}>
            <label className="form-label">{idx + 1}. {q}</label>
            <div className="form-options">
              {options.map((opt, v) => (
                <label key={opt} className="form-radio">
                  <input
                    type="radio"
                    name={`q${idx + 1}`}
                    value={v}
                    checked={answers[`q${idx + 1}`] === v}
                    onChange={() => handleChange(`q${idx + 1}`, v)}
                    required
                  />
                  <span>{opt}</span>
                </label>
              ))}
            </div>
          </div>
        ))}
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

export default Phq9Form;
