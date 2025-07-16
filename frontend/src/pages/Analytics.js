import React, { useEffect, useState } from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

const Analytics = () => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        console.log("🔍 Fetching analytics from:", `${process.env.REACT_APP_API_URL}/analytics/summary`);
        
        const response = await fetch(`${process.env.REACT_APP_API_URL}/analytics/summary`, {
          headers: {
            'ngrok-skip-browser-warning': 'true',
            'Content-Type': 'application/json'
          }
        });
        
        console.log("📡 Response status:", response.status);
        console.log("📡 Response headers:", response.headers.get('content-type'));
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
          const text = await response.text();
          console.error("❌ Non-JSON response:", text);
          throw new Error('Server returned non-JSON response');
        }
        
        const result = await response.json();
        console.log("✅ Analytics data received:", result);
        setData(result);
        setError(null);
        
      } catch (err) {
        console.error("❌ Failed to fetch analytics:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalytics();
  }, []);

  if (loading) return <div className="text-center text-gray-500">Loading analytics...</div>;
  if (error) return <div className="text-center text-red-500">Error: {error}</div>;
  if (!data) return <div className="text-center text-gray-500">No data available</div>;

  // Check if data has any values > 0
  const hasData = Object.values(data).some(value => value > 0);
  
  if (!hasData) {
    return (
      <div className="max-w-md mx-auto py-10 text-center">
        <h2 className="text-2xl font-bold mb-4">📊 Application Status</h2>
        <p className="text-gray-500">No job applications found. Start applying to see your analytics!</p>
      </div>
    );
  }

  const chartData = {
    labels: Object.keys(data).map(key => key.charAt(0).toUpperCase() + key.slice(1)),
    datasets: [{
      data: Object.values(data),
      backgroundColor: [
        '#3498db', // Applied - Blue
        '#f39c12', // Interview - Orange
        '#2ecc71', // Offer - Green
        '#e74c3c'  // Rejected - Red
      ],
      borderWidth: 2,
      borderColor: '#fff'
    }]
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          padding: 20,
          usePointStyle: true
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            const label = context.label || '';
            const value = context.parsed || 0;
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
            return `${label}: ${value} (${percentage}%)`;
          }
        }
      }
    }
  };

  return (
    <div className="max-w-md mx-auto py-10">
      <h2 className="text-2xl font-bold text-center mb-6">📊 Application Status</h2>
      <Pie data={chartData} options={options} />
      
      {/* Summary stats */}
      <div className="mt-6 grid grid-cols-2 gap-4">
        {Object.entries(data).map(([status, count]) => (
          <div key={status} className="bg-gray-100 rounded-lg p-3 text-center">
            <div className="text-2xl font-bold text-gray-700">{count}</div>
            <div className="text-sm text-gray-600 capitalize">{status}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Analytics;