import React, { useState } from 'react';

const NihssForm: React.FC = () => {
    const [formData, setFormData] = useState({
        nihs_1: '', nihs_2: '', nihs_3: '', nihs_4: '', nihs_5: '',
        nihs_6: '', nihs_7: '', nihs_8: '', nihs_9: '', nihs_10: '', nihs_11: ''
    });
    const [result, setResult] = useState<string | null>(null);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            const response = await fetch('/nihss/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            const data = await response.json();
            setResult(data.severity);
        } catch (error) {
            console.error('Error:', error);
        }
    };

    return (
        <div className="max-w-md mx-auto p-4 bg-white shadow-md rounded-md">
            <h1 className="text-xl font-bold mb-4">NIHSS Stroke Severity Prediction</h1>
            <form onSubmit={handleSubmit} className="space-y-4">
                {Object.keys(formData).map((key) => (
                    <div key={key} className="flex flex-col">
                        <label className="mb-1 font-medium" htmlFor={key}>{key.replace('_', ' ').toUpperCase()}:</label>
                        <input
                            type="number"
                            id={key}
                            name={key}
                            value={formData[key as keyof typeof formData]}
                            onChange={handleChange}
                            min="0"
                            max="4"
                            required
                            className="border border-gray-300 rounded-md p-2"
                        />
                    </div>
                ))}
                <button type="submit" className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600">Predict Severity</button>
            </form>
            {result && (
                <div className="mt-4 p-4 bg-green-100 text-green-800 rounded-md">
                    Predicted Severity: {result}
                </div>
            )}
        </div>
    );
};

export default NihssForm;
