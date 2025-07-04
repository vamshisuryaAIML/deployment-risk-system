import pandas as pd

def extract_features(deployment_change):
    features = {
        "lines_added": deployment_change.get("lines_added", 0),
        "lines_deleted": deployment_change.get("lines_deleted", 0),
        "files_changed": deployment_change.get("files_changed", 0),
        "services_affected": deployment_change.get("services_affected", 1),
        "risk_score": deployment_change.get("risk_score", 0.5),
    }
    return pd.DataFrame([features])

def monitor_post_deployment(metrics):
    anomalies = []
    if metrics.get('error_rate', 0) > 0.05:
        anomalies.append('High error rate')
    if metrics.get('latency_ms', 0) > 500:
        anomalies.append('High latency')
    if metrics.get('cpu_usage', 0) > 0.9:
        anomalies.append('High CPU usage')
    return anomalies

def rollback_decision(risk_prob, anomalies, risk_threshold=0.7):
    if risk_prob > risk_threshold:
        return True, f"High predicted rollback risk ({risk_prob:.2f})"
    if anomalies:
        return True, f"Detected anomalies post deployment: {anomalies}"
    return False, "Deployment stable"
