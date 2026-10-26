import { useEffect, useState } from 'react';
import axios from 'axios';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import './App.css';

interface Metrics {
  MAE: number;
  RMSE: number;
  MAPE: number;
}

interface TimeSeriesData {
  startTime: string;
  actual_generation: number;
  forecast_generation: number;
}

function App() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [data, setData] = useState<TimeSeriesData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [metricsRes, dataRes] = await Promise.all([
          axios.get('http://127.0.0.1:8000/api/metrics'),
          axios.get('http://127.0.0.1:8000/api/timeseries')
        ]);
        
        setMetrics(metricsRes.data);
        
        const formattedData = dataRes.data.map((item: TimeSeriesData) => ({
          ...item,
          formattedTime: new Date(item.startTime).toLocaleString('en-GB', { 
            day: 'numeric', month: 'short', hour: '2-digit', minute:'2-digit' 
          })
        }));
        
        setData(formattedData);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching data:", error);
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="loading">Loading Dashboard Data...</div>;
  }

  return (
    <div className="dashboard-container">
      <header>
        <h1>UK Wind Generation Forecast Dashboard</h1>
        <p>Day-Ahead Market Analysis (January 2026)</p>
      </header>

      {/* KPI Metrics Cards */}
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Mean Absolute Error (MAE)</h3>
          <p className="metric-value">{metrics?.MAE} <span className="unit">MW</span></p>
          <p className="metric-desc">Average magnitude of forecast errors.</p>
        </div>
        <div className="metric-card">
          <h3>Root Mean Square Error (RMSE)</h3>
          <p className="metric-value">{metrics?.RMSE} <span className="unit">MW</span></p>
          <p className="metric-desc">Penalizes larger errors more heavily.</p>
        </div>
        <div className="metric-card">
          <h3>Mean Abs. Percentage Error (MAPE)</h3>
          <p className="metric-value">{metrics?.MAPE} <span className="unit">%</span></p>
          <p className="metric-desc">Average percentage deviation.</p>
        </div>
      </div>

      {/* Chart Section */}
      <div className="chart-container">
        <h2>Actual vs Forecasted Wind Generation</h2>
        <div className="chart-wrapper">
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" opacity={0.3} />
              <XAxis 
                dataKey="formattedTime" 
                minTickGap={50}
                tick={{ fontSize: 12 }} 
              />
              <YAxis 
                label={{ value: 'Generation (MW)', angle: -90, position: 'insideLeft' }} 
              />
              <Tooltip />
              <Legend verticalAlign="top" height={36}/>
              <Line 
                type="monotone" 
                dataKey="actual_generation" 
                name="Actual Generation" 
                stroke="#10b981" 
                strokeWidth={2}
                dot={false} 
              />
              <Line 
                type="monotone" 
                dataKey="forecast_generation" 
                name="Forecasted Generation" 
                stroke="#3b82f6" 
                strokeWidth={2}
                dot={false} 
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default App;