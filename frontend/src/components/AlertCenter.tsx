import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AlertCenter = () => {
    const [alerts, setAlerts] = useState([]);
    const [filter, setFilter] = useState('');

    useEffect(() => {
        // Fetch recent alerts
        axios.get('/api/alerts/recent')
            .then(response => setAlerts(response.data))
            .catch(error => console.error('Error fetching alerts:', error));
    }, []);

    const handleFilterChange = (event) => {
        setFilter(event.target.value);
    };

    const handleTestAlert = async () => {
        try {
            await axios.post('/api/alert/test', {
                user_id: 1, // Replace with dynamic user ID
                message: 'Test alert message',
                method: 'email', // or 'telegram'
            });
            alert('Test alert sent successfully!');
        } catch (error) {
            console.error('Error sending test alert:', error);
        }
    };

    const filteredAlerts = alerts.filter(alert =>
        filter ? alert.type === filter : true
    );

    return (
        <div className="alert-center">
            <h2>Alert Center</h2>

            <div className="filter">
                <label htmlFor="filter">Filter by type:</label>
                <select id="filter" value={filter} onChange={handleFilterChange}>
                    <option value="">All</option>
                    <option value="BP">Blood Pressure</option>
                    <option value="PHQ">PHQ-9</option>
                    <option value="Barthel">Barthel</option>
                    <option value="NIHSS">NIHSS</option>
                </select>
            </div>

            <ul className="alerts">
                {filteredAlerts.map((alert, index) => (
                    <li key={index}>
                        <strong>{alert.type}:</strong> {alert.message}
                    </li>
                ))}
            </ul>

            <button onClick={handleTestAlert}>Send Test Alert</button>
        </div>
    );
};

export default AlertCenter;
