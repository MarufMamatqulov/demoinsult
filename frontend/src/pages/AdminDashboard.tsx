import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const AdminDashboard = () => {
    const [patients, setPatients] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        // Fetch list of all patients
        axios.get('/api/patients')
            .then(response => setPatients(response.data))
            .catch(error => console.error('Error fetching patients:', error));
    }, []);

    const handleDetailsClick = (patientId) => {
        navigate(`/admin/patient/${patientId}`);
    };

    return (
        <div className="admin-dashboard">
            <h2>Admin Dashboard</h2>

            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Age</th>
                        <th>Last Assessment</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {patients.map(patient => (
                        <tr key={patient.id}>
                            <td>{patient.name}</td>
                            <td>{patient.age}</td>
                            <td>{patient.lastAssessment}</td>
                            <td>
                                <button onClick={() => handleDetailsClick(patient.id)}>Details</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const PatientDetails = ({ patientId }) => {
    const [patientData, setPatientData] = useState(null);
    const [recommendations, setRecommendations] = useState([]);

    useEffect(() => {
        // Fetch patient details
        axios.get(`/api/patients/${patientId}`)
            .then(response => setPatientData(response.data))
            .catch(error => console.error('Error fetching patient details:', error));

        // Fetch recommendations
        axios.post('/api/recommendations/generate', { patientId })
            .then(response => setRecommendations(response.data))
            .catch(error => console.error('Error fetching recommendations:', error));
    }, [patientId]);

    const handleGeneratePDF = () => {
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

    if (!patientData) return <div>Loading...</div>;

    return (
        <div className="patient-details">
            <h2>{patientData.name}'s Details</h2>

            <div className="trend-charts">
                <h3>Trend Charts</h3>
                {/* Add trend chart components here */}
            </div>

            <div className="recommendations">
                <h3>Recommendations</h3>
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

export { AdminDashboard, PatientDetails };
