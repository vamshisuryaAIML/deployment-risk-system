import React, { useState } from "react";

export default function DeploymentForm({ onSubmit }) {
  const [deploymentChange, setDeploymentChange] = useState({
    lines_added: 0,
    lines_deleted: 0,
    files_changed: 0,
    services_affected: 1,
    risk_score: 0.5,
  });

  const [postMetrics, setPostMetrics] = useState({
    error_rate: 0,
    latency_ms: 0,
    cpu_usage: 0,
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ deployment_change: deploymentChange, post_metrics: postMetrics });
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>Deployment Change</h3>
      {Object.keys(deploymentChange).map((key) => (
        <div key={key}>
          <label>{key}:</label>
          <input
            type="number"
            value={deploymentChange[key]}
            onChange={(e) =>
              setDeploymentChange({ ...deploymentChange, [key]: Number(e.target.value) })
            }
          />
        </div>
      ))}

      <h3>Post Deployment Metrics</h3>
      {Object.keys(postMetrics).map((key) => (
        <div key={key}>
          <label>{key}:</label>
          <input
            type="number"
            step="0.01"
            value={postMetrics[key]}
            onChange={(e) =>
              setPostMetrics({ ...postMetrics, [key]: Number(e.target.value) })
            }
          />
        </div>
      ))}

      <button type="submit">Predict Rollback Risk</button>
    </form>
  );
}
