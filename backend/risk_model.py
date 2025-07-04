import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

class RiskModel:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = LogisticRegression()
        self.is_trained = False
    
    def train(self, X, y):
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True
    
    def predict_risk(self, features_df):
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        X_scaled = self.scaler.transform(features_df)
        prob = self.model.predict_proba(X_scaled)[:,1]
        return prob[0]
