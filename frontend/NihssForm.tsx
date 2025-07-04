// filepath: c:\Users\Marufjon\InsultMedAI\frontend\NihssForm.tsx.new
import React, { useState } from 'react';
import './AssessmentForms.css';
import { useTranslation } from 'react-i18next';
// Import AIRecommendations component with correct path
import AIRecommendations from './src/AIRecommendations.tsx';

const NihssForm = () => {
    const { t } = useTranslation();
    const [formData, setFormData] = useState({
        nihs_1: '0', nihs_2: '0', nihs_3: '0', nihs_4: '0', nihs_5: '0',
        nihs_6: '0', nihs_7: '0', nihs_8: '0', nihs_9: '0', nihs_10: '0', nihs_11: '0'
    });
    const [result, setResult] = useState('');
    const [loading, setLoading] = useState(false);
    const [submitted, setSubmitted] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        
        try {
            // Convert string values to numbers
            const numericFormData = {};
            Object.entries(formData).forEach(([key, value]) => {
                numericFormData[key] = parseInt(value, 10);
            });

            const response = await fetch('http://localhost:8000/nihss/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(numericFormData)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            if (data && data.severity) {
                setResult(data.severity);
            } else {
                setResult("Unable to provide detailed analysis. Please consult with your healthcare provider.");
            }
            setSubmitted(true);
        } catch (error) {
            console.error('Error:', error);
            setResult("An error occurred while analyzing the data. Please try again.");
            setSubmitted(true);
        } finally {
            setLoading(false);
        }
    };

    // Define explanations for each NIHSS item
    const nihssOptions = [
        { label: "Level of Consciousness", scoringGuide: "0: Alert, 1: Drowsy, 2: Stuporous, 3: Coma" },
        { label: "LOC Questions", scoringGuide: "0: Answers both correctly, 1: Answers one correctly, 2: Answers none correctly" },
        { label: "LOC Commands", scoringGuide: "0: Performs both tasks, 1: Performs one task, 2: Performs neither task" },
        { label: "Best Gaze", scoringGuide: "0: Normal, 1: Partial gaze palsy, 2: Total gaze palsy" },
        { label: "Visual Fields", scoringGuide: "0: No visual loss, 1: Partial hemianopia, 2: Complete hemianopia, 3: Bilateral hemianopia" },
        { label: "Facial Palsy", scoringGuide: "0: Normal, 1: Minor paralysis, 2: Partial paralysis, 3: Complete paralysis" },
        { label: "Motor Arm - Left", scoringGuide: "0: No drift, 1: Drift, 2: Some effort against gravity, 3: No effort against gravity, 4: No movement" },
        { label: "Motor Arm - Right", scoringGuide: "0: No drift, 1: Drift, 2: Some effort against gravity, 3: No effort against gravity, 4: No movement" },
        { label: "Motor Leg - Left", scoringGuide: "0: No drift, 1: Drift, 2: Some effort against gravity, 3: No effort against gravity, 4: No movement" },
        { label: "Motor Leg - Right", scoringGuide: "0: No drift, 1: Drift, 2: Some effort against gravity, 3: No effort against gravity, 4: No movement" },
        { label: "Ataxia", scoringGuide: "0: Absent, 1: Present in one limb, 2: Present in two limbs" }
    ];

    const calculateTotalScore = (): number => {
        return Object.values(formData).reduce((total: number, val: string) => total + parseInt(val || '0', 10), 0);
    };

    return (
        <div className="medical-form-container animate-fade-in nihss-form">
            <h2 className="form-title">NIHSS Stroke Scale</h2>
            <p className="form-description">Assess stroke severity using the NIHSS scale.</p>

            {!submitted ? (
                <form onSubmit={handleSubmit} className="assessment-form">
                    {nihssOptions.map((option, index) => (
                        <div key={index} className="form-group">
                            <label htmlFor={`nihs_${index + 1}`}>{option.label}</label>
                            <div className="scoring-guide">{option.scoringGuide}</div>
                            <select
                                id={`nihs_${index + 1}`}
                                name={`nihs_${index + 1}`}
                                value={formData[`nihs_${index + 1}` as keyof typeof formData]}
                                onChange={handleChange}
                                required
                            >
                                <option value="0">0</option>
                                <option value="1">1</option>
                                <option value="2">2</option>
                                {(index > 5 && index < 10) || index === 3 ? <option value="3">3</option> : null}
                                {(index > 5 && index < 10) ? <option value="4">4</option> : null}
                            </select>
                        </div>
                    ))}

                    <div className="total-score">
                        <span>Total Score: {calculateTotalScore()}</span>
                    </div>

                    <button type="submit" className="submit-button" disabled={loading}>
                        {loading ? "Loading..." : "Submit"}
                    </button>
                </form>
            ) : (
                <div className="results-container">
                    <h3>Assessment Results</h3>
                    <div className="results-content">
                        <div className="score-display">
                            <span>Total Score: {calculateTotalScore()}</span>
                            <span>Severity: {result}</span>
                        </div>
                    </div>
                    <div className="ai-recommendations-section">
                        <h3>AI Recommendations</h3>
                        <AIRecommendations 
                            assessmentType="nihss"
                            assessmentData={{
                                scores: formData,
                                totalScore: calculateTotalScore(),
                                severity: result
                            }}
                            language="en"
                        />
                    </div>
                    
                    <button 
                        className="reset-button"
                        onClick={() => setSubmitted(false)}
                    >
                        New Assessment
                    </button>
                </div>
            )}
        </div>
    );
};

export default NihssForm;
