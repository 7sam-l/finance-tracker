import { useState, useEffect } from "react";
import { api } from "../services/api";
import {
  LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

function Insights() {
  const [trends, setTrends] = useState(null);
  const [forecastSummary, setForecastSummary] = useState(null);
  const [categoryForecast, setCategoryForecast] = useState(null);
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadData() {
      try {
        const [tData, fsData, fcData, aData] = await Promise.all([
          api.getAnalyticsTrends(),
          api.getForecastSummary(),
          api.getForecastByCategory(),
          api.getAnalyticsAnomalies()
        ]);
        
        // Format trends data for Recharts
        const chartData = tData.months.map((month, index) => {
            const dataPoint = { name: month, Overall: tData.overall[index] };
            Object.keys(tData.by_category).forEach(cat => {
                dataPoint[cat] = tData.by_category[cat][index];
            });
            return dataPoint;
        });

        setTrends({ raw: tData, chartData });
        setForecastSummary(fsData);
        setCategoryForecast(fcData.forecast);
        setAnomalies(aData);
      } catch (err) {
        setError("Failed to load insights data.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <div className="loading">Loading insights...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="insights-page">
      <h2>Data Science Insights</h2>
      
      <div className="forecast-summary-card">
        <h3>Forecast for Next Month ({forecastSummary?.month})</h3>
        <p>Method: {forecastSummary?.method.replace('_', ' ')}</p>
        <div className="forecast-stats">
            <div className="stat">
                <span className="label">Expected Expenses:</span>
                <span className="value expense">₹{forecastSummary?.predicted_total_expense.toFixed(2)}</span>
            </div>
            <div className="stat">
                <span className="label">Expected Income:</span>
                <span className="value income">₹{forecastSummary?.predicted_total_income.toFixed(2)}</span>
            </div>
            <div className="stat">
                <span className="label">Expected Net:</span>
                <span className="value">₹{forecastSummary?.predicted_net.toFixed(2)}</span>
            </div>
        </div>
        <div className="confidence-interval">
            <small>95% Confidence Interval for Expenses: ₹{forecastSummary?.confidence_interval[0].toFixed(2)} - ₹{forecastSummary?.confidence_interval[1].toFixed(2)}</small>
        </div>
      </div>

      <div className="charts-grid">
        <div className="chart-container">
            <h3>Spending Trends (Last 12 Months)</h3>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={trends?.chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="Overall" stroke="#8884d8" strokeWidth={3} />
                    {trends && Object.keys(trends.raw.by_category).slice(0, 5).map((cat, i) => {
                        const colors = ["#82ca9d", "#ffc658", "#ff7300", "#0088FE", "#00C49F"];
                        return <Line key={cat} type="monotone" dataKey={cat} stroke={colors[i % colors.length]} strokeWidth={1} />
                    })}
                </LineChart>
            </ResponsiveContainer>
        </div>

        <div className="chart-container">
            <h3>Category Forecast (Next Month)</h3>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={categoryForecast}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="category" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="predicted_amount" fill="#82ca9d" name="Predicted Amount" />
                </BarChart>
            </ResponsiveContainer>
        </div>
      </div>

      <div className="anomalies-section">
        <h3>Recent Anomalies Detected</h3>
        {anomalies.length === 0 ? (
            <p>No unusual transactions detected recently.</p>
        ) : (
            <ul className="anomalies-list">
                {anomalies.map(a => (
                    <li key={a.transaction_id} className="anomaly-item">
                        <div className="anomaly-header">
                            <strong>{a.description}</strong> - ₹{a.amount}
                            <span className="date">{new Date(a.date).toLocaleDateString()}</span>
                        </div>
                        <div className="anomaly-reason">
                            ⚠️ {a.reason}
                        </div>
                    </li>
                ))}
            </ul>
        )}
      </div>
    </div>
  );
}

export default Insights;
