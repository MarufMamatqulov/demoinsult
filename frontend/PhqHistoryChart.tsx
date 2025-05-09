import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
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

const PhqHistoryChart: React.FC<{ patientId: string }> = ({ patientId }) => {
    const [data, setData] = useState<any>(null);
    const [daysFilter, setDaysFilter] = useState(30);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`/history/phq/${patientId}?days=${daysFilter}`);
                const result = await response.json();
                setData(result);
            } catch (error) {
                console.error('Error fetching PHQ-9 history:', error);
            }
        };

        fetchData();
    }, [daysFilter, patientId]);

    const formatChartData = () => {
        if (!data) return null;

        const labels = data.map((entry: any) => new Date(entry.created_at).toLocaleDateString());
        const scores = data.map((entry: any) => entry.score);

        return {
            labels,
            datasets: [
                {
                    label: 'PHQ-9 Score',
                    data: scores,
                    borderColor: scores.map((score: number) => {
                        if (score < 5) return 'green';
                        if (score >= 10 && score <= 14) return 'orange';
                        if (score >= 20) return 'red';
                        return 'blue';
                    }),
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                },
            ],
        };
    };

    return (
        <div className="max-w-4xl mx-auto p-4">
            <div className="flex justify-between mb-4">
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
                <Line data={formatChartData()} options={{ responsive: true }} />
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
};

export default PhqHistoryChart;
