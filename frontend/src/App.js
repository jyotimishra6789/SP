import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // More deterministic human-like values
  const generateHumanLikeData = () => {
    const avg_speed = 120 + Math.random() * 30;
    const max_speed = 250 + Math.random() * 50;
    const min_speed = 5 + Math.random() * 5;
    const std_speed = 20 + Math.random() * 15;

    const acceleration_mean = 0 + Math.random() * 10;
    const acceleration_std = 30 + Math.random() * 10;

    const curvature_mean = 2.5 + Math.random() * 2;

    const num_events = Math.floor(80 + Math.random() * 20);
    const event_clicks = Math.floor(3 + Math.random() * 2);

    const time_span = 12 + Math.random() * 4;
    const click_rate = event_clicks / time_span;
    const time_per_event = time_span / num_events;
    const clicks_per_event = event_clicks / num_events;
    const click_interval_mean = event_clicks > 1 ? time_span / (event_clicks - 1) : 0;

    return {
      avg_speed,
      max_speed,
      min_speed,
      std_speed,
      acceleration_mean,
      acceleration_std,
      curvature_mean,
      num_events,
      event_clicks,
      click_rate,
      time_span,
      click_interval_mean,
      time_per_event,
      clicks_per_event
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
