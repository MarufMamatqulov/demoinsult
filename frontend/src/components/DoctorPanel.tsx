import React, { useEffect, useState } from 'react';
import axios from 'axios';

const DoctorPanel = () => {
    const [assessmentData, setAssessmentData] = useState([]);
    const [recommendations, setRecommendations] = useState([]);

    useEffect(() => {
        // Fetch last 7 days of assessment data
        axios.get('/api/assessments/last-7-days')
            .then(response => setAssessmentData(response.data))
            .catch(error => console.error('Error fetching assessment data:', error));

        // Fetch auto-generated recommendations
        axios.post('/api/recommendations/generate', { /* Add necessary payload */ })
            .then(response => setRecommendations(response.data))
            .catch(error => console.error('Error fetching recommendations:', error));
    }, []);

    const handleGeneratePDF = () => {
        const patientId = 123; // Replace with dynamic patient ID
        axios.get(`/api/report/pdf/${patientId}`, { responseType: 'blob' })
            .then(response => {
                const url = window.URL.createObjectURL(new Blob([response.data]));
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', `Patient_Report_${patientId}.pdf`);
                document.body.appendChild(link);
                link.click();
                link.remove();
            })
            .catch(error => console.error('Error generating PDF report:', error));
    };

    return (
        <div className="doctor-panel">
            <h2>Doctor Panel</h2>

            <div className="assessment-data">
                <h3>Last 7 Days Assessment Data</h3>
                <ul>
                    {assessmentData.map((data, index) => (
                        <li key={index}>{JSON.stringify(data)}</li>
                    ))}
                </ul>
            </div>

            <div className="recommendations">
                <h3>Auto-Generated Recommendations</h3>
                <ul>
                    {recommendations.map((rec, index) => (
                        <li key={index}>{rec}</li>
                    ))}
                </ul>
            </div>

            <button onClick={handleGeneratePDF}>Generate PDF Report</button>
        </div>
    );
};

export default DoctorPanel;
