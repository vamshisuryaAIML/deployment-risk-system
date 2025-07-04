import React, { useState } from "react";
import DeploymentForm from "./components/DeploymentForm";
import './App.css';

function App() {
  const [result, setResult] = useState(null);

  const handlePredict = async (data) => {
    try {
      const res = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const json = await res.json();
      setResult(json);
    } catch (error) {
      alert("Error connecting to backend");
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Deployment Risk Assessment</h1>
      <DeploymentForm onSubmit={handlePredict} />
      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>Prediction Result:</h3>
          <p>Rollback Probability: {(result.risk_probability * 100).toFixed(2)}%</p>
          <p>Anomalies Detected: {result.anomalies.length ? result.anomalies.join(", ") : "None"}</p>
          <p>Rollback Decision: {result.rollback ? "YES" : "NO"}</p>
          <p>Reason: {result.reason}</p>
        </div>
      )}
    </div>
  );
}

export default App;
