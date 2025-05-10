import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import './FormMedical.css';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

export default function HistoryChart({ patientId }) {
    const [data, setData] = useState(null);
    const [chartType, setChartType] = useState('blood-pressure');
    const [daysFilter, setDaysFilter] = useState(30);
    const [alert, setAlert] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(
                    `/history/${chartType}/${patientId}?days=${daysFilter}`
                );
                const result = await response.json();
                setData(result);

                // Fetch alert for blood pressure trends if applicable
                if (chartType === 'blood-pressure') {
                    const alertResponse = await fetch('/alerts/analyze-bp', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(result),
                    });
                    const alertData = await alertResponse.json();
                    setAlert(alertData);
                } else {
                    setAlert(null);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, [chartType, daysFilter, patientId]);

    const formatChartData = () => {
        if (!data) return null;

        const labels = data.map((entry) => new Date(entry.measurement_time).toLocaleDateString());
        const values = data.map((entry) =>
            chartType === 'blood-pressure' ? entry.systolic : entry.value || entry.score
        );

        return {
            labels,
            datasets: [
                {
                    label: chartType === 'blood-pressure' ? 'Systolic BP' : 'Value',
                    data: values,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                },
            ],
        };
    };

    const getAlertColor = () => {
        if (!alert) return '';
        switch (alert.status) {
            case 'Danger':
                return 'text-red-600';
            case 'Rising':
                return 'text-yellow-600';
            case 'Fluctuating':
                return 'text-yellow-600';
            case 'Stable':
                return 'text-green-600';
            default:
                return '';
        }
    };

    // Example data, replace with real API data
    const chartData = {
        labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'],
        datasets: [
            {
                label: 'PHQ-9 Score',
                data: [5, 7, 6, 8, 4],
                fill: false,
                backgroundColor: '#00796b',
                borderColor: '#26c6da',
                tension: 0.3,
                pointRadius: 6,
                pointHoverRadius: 9,
            },
        ],
    };

    const options = {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                labels: { color: '#00796b', font: { size: 16, weight: 'bold' as const } },
            },
            title: {
                display: true,
                text: 'PHQ-9 Score Trend',
                color: '#00796b',
                font: { size: 22, weight: 'bold' as const },
            },
        },
        scales: {
            x: {
                ticks: { color: '#00796b', font: { size: 14 } },
                grid: { color: '#b2dfdb' },
            },
            y: {
                beginAtZero: true,
                ticks: { color: '#00796b', font: { size: 14 } },
                grid: { color: '#b2dfdb' },
            },
        },
        animation: {
            duration: 1200,
        },
    };

    return (
        <div className="medical-form-container animate-fade-in max-w-4xl mx-auto p-4">
            <h2 className="form-title">History and Trends</h2>
            <div className="flex justify-between mb-4">
                <select
                    value={chartType}
                    onChange={(e) => setChartType(e.target.value)}
                    className="border border-gray-300 rounded-md p-2"
                >
                    <option value="blood-pressure">Blood Pressure</option>
                    <option value="nihss">NIHSS</option>
                    <option value="barthel">Barthel Index</option>
                </select>
                <select
                    value={daysFilter}
                    onChange={(e) => setDaysFilter(Number(e.target.value))}
                    className="border border-gray-300 rounded-md p-2"
                >
                    <option value={7}>Last 7 Days</option>
                    <option value={30}>Last 30 Days</option>
                    <option value={90}>Last 90 Days</option>
                </select>
            </div>
            {data ? (
                <div style={{ background: '#fff', borderRadius: '16px', padding: '1.5rem', boxShadow: '0 2px 8px rgba(0,121,107,0.08)' }}>
                    <Line data={chartData} options={options} />
                </div>
            ) : (
                <p>Loading...</p>
            )}
            {alert && (
                <div className={`mt-4 p-4 rounded-md ${getAlertColor()}`}>
                    <p><strong>Status:</strong> {alert.status}</p>
                    <p><strong>Warning:</strong> {alert.warning}</p>
                </div>
            )}
        </div>
    );
};
