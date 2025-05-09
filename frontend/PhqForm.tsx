import React, { useState } from 'react';
import axios from 'axios';

const PhqForm: React.FC = () => {
    const [formData, setFormData] = useState({
        q1: 0,
        q2: 0,
        q3: 0,
        q4: 0,
        q5: 0,
        q6: 0,
        q7: 0,
        q8: 0,
        q9: 0
    });
    const [result, setResult] = useState<string | null>(null);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: parseInt(value) });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await axios.post('/phq/analyze', formData);
            setResult(response.data.prediction);
        } catch (error) {
            console.error('Error submitting form:', error);
            setResult('Error analyzing PHQ-9 data');
        }
    };

    return (
        <div className="max-w-md mx-auto p-4 bg-white shadow-md rounded">
            <h1 className="text-xl font-bold mb-4">PHQ-9 Depression Analysis</h1>
            <form onSubmit={handleSubmit} className="space-y-4">
                {Array.from({ length: 9 }, (_, i) => (
                    <div key={i} className="flex items-center space-x-4">
                        <label htmlFor={`q${i + 1}`} className="w-16 font-medium">Q{i + 1}</label>
                        <input
                            type="range"
                            id={`q${i + 1}`}
                            name={`q${i + 1}`}
                            min="0"
                            max="3"
                            value={formData[`q${i + 1}`]}
                            onChange={handleChange}
                            className="flex-1"
                        />
                        <span className="w-8 text-center">{formData[`q${i + 1}`]}</span>
                    </div>
                ))}
                <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded hover:bg-blue-600">Submit</button>
            </form>
            {result && (
                <div className="mt-4 p-4 bg-gray-100 rounded">
                    <h2 className="text-lg font-semibold">Result</h2>
                    <p className="text-gray-700">Depression Level: <strong>{result}</strong></p>
                </div>
            )}
        </div>
    );
};

export default PhqForm;
