from flask import Flask, request, jsonify
from flask_cors import CORS


from risk_model import RiskModel
from utils import extract_features, monitor_post_deployment, rollback_decision

app = Flask(__name__)

CORS(app)  # <--- enable CORS for all routes

# Initialize and train model once on startup (using dummy data)
risk_model = RiskModel()
training_data = [
    {"lines_added": 100, "lines_deleted": 20, "files_changed": 5, "services_affected": 1, "risk_score": 0.2},
    {"lines_added": 500, "lines_deleted": 100, "files_changed": 15, "services_affected": 3, "risk_score": 0.7},
    {"lines_added": 50, "lines_deleted": 10, "files_changed": 3, "services_affected": 1, "risk_score": 0.1},
    {"lines_added": 1000, "lines_deleted": 300, "files_changed": 25, "services_affected": 5, "risk_score": 0.9},
]
labels = [0, 1, 0, 1]

import pandas as pd
training_df = pd.DataFrame(training_data)
risk_model.train(training_df, labels)


@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    deployment_change = data.get('deployment_change', {})
    post_metrics = data.get('post_metrics', {})
    
    features_df = extract_features(deployment_change)
    risk_prob = risk_model.predict_risk(features_df)
    anomalies = monitor_post_deployment(post_metrics)
    should_rollback, reason = rollback_decision(risk_prob, anomalies)
    
    return jsonify({
        "risk_probability": risk_prob,
        "anomalies": anomalies,
        "rollback": should_rollback,
        "reason": reason
    })

if __name__ == '__main__':
    app.run(debug=True)
