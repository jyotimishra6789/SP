import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // More deterministic human-like values
  const generateHumanLikeData = () => {
    // Generate data that matches the true human statistical distribution
    return {
      avg_speed: 2.6 + (Math.random() - 0.5) * 1.5,
      max_speed: 18.1 + (Math.random() - 0.5) * 10,
      min_speed: 0,
      std_speed: 3.5 + (Math.random() - 0.5) * 2,
      acceleration_mean: 0.02 + (Math.random() - 0.5) * 0.05,
      acceleration_std: 3.6 + (Math.random() - 0.5) * 2,
      curvature_mean: 76000 + (Math.random() - 0.5) * 10000,
      num_events: Math.floor(85 + (Math.random() * 25)),
      event_clicks: 0,
      click_rate: 0,
      time_span: 600 + Math.random() * 50,
      click_interval_mean: 0,
      time_per_event: 5.6 + (Math.random() - 0.5) * 2,
      clicks_per_event: 0
    };
  };

  const simulateBehavior = () => {
    setLoading(true);
    setResult(null);

    const behaviorData = generateHumanLikeData();

    axios.post('http://127.0.0.1:5000/predict', behaviorData, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then((res) => {
        setResult(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("API Error:", err.response?.data || err.message);
        setResult("API Error");
        setLoading(false);
      });
  };

  return (
    <div className="App" style={{ padding: '2rem', fontFamily: 'Arial' }}>
      <h1>🛡️ SentinelPay - AI Trust Detector</h1>
      <p>Simulate user behavioral patterns to detect bots in real-time at checkout.</p>

      <button
        onClick={simulateBehavior}
        style={{
          padding: '10px 20px',
          fontSize: '16px',
          backgroundColor: '#4CAF50',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer'
        }}
      >
        Simulate User
      </button>

      {loading && <p style={{ marginTop: '1rem' }}>⏳ Evaluating behavior...</p>}

      {result && !loading && result !== "API Error" && (
        <div style={{ marginTop: '2rem' }}>
          <h2>
            Trust Score: <span style={{ color: result.trust_score > 0.7 ? 'green' : 'orange' }}>
              {Math.round(result.trust_score * 100)}%
            </span>
          </h2>
          <h3>
            Prediction:&nbsp;
            <span style={{
              backgroundColor: result.prediction === 1 ? 'green' : 'red',
              color: 'white',
              padding: '4px 10px',
              borderRadius: '5px'
            }}>
              {result.label}
            </span>
          </h3>
        </div>
      )}

      {result === "API Error" && !loading && (
        <h2 style={{ color: 'red', marginTop: '2rem' }}>❌ API Error</h2>
      )}
    </div>
  );
}

export default App;
