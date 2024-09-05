// src/components/PieChart.js

import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, ArcElement);

const PieChart = ({ data }) => {
    const chartData = {
        labels: ['Positive Reviews', 'Negative Reviews', 'Neutral Reviews'],
        datasets: [
            {
                data: [data.Positive, data.Negative, data.Neutral],
                backgroundColor: ['#4caf50', '#f44336', '#9e9e9e'],
                borderColor: '#fff',
                borderWidth: 2,
            },
        ],
    };

    return (
        <div className="w-full max-w-md mx-auto my-8">
            <h2 className="text-xl font-bold text-center mb-4">Review Sentiment Breakdown</h2>
            <Pie data={chartData} />
        </div>
    );
};

export default PieChart;
