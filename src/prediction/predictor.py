"""
Prediction module for CIT Loss Prediction
"""

import pickle
import os
import pandas as pd

class Predictor:
    def __init__(self, model_path='models/xgboost_model.pkl'):
        self.model_path = model_path
        self.model = self.load_model()
        self.model_loaded = self.model is not None
    
    def load_model(self):
        """Load trained model"""
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, 'rb') as f:
                    return pickle.load(f)
            return None
        except Exception as e:
            print(f"Error loading model: {e}")
            return None
    
    def predict_single(self, features):
        """Predict single instance"""
        if not self.model_loaded:
            return {'error': 'Model not loaded'}
        
        # Convert features to DataFrame
        df = pd.DataFrame([features])
        
        # Make prediction
        prediction = self.model.predict(df)[0]
        probability = self.model.predict_proba(df)[0][1]
        
        return {
            'prediction': int(prediction),
            'probability': float(probability),
            'risk_level': 'High' if prediction == 1 else 'Low'
        }
