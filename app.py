"""
CIT Loss Prediction System - Web Application
Complete version with all routes
"""
from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import xgboost as xgb
import io
import csv

app = Flask(__name__)

# Global variables for model
MODEL = None
FEATURE_NAMES = None
THRESHOLD = 0.5

def load_model():
    """Load the trained model"""
    global MODEL, FEATURE_NAMES, THRESHOLD
    
    try:
        model_path = "deployment_artifacts/kra_cit_risk_model_v1.pkl"
        
        if not os.path.exists(model_path):
            return False, "Model file not found"
        
        print(f"Loading model from: {model_path}")
        bundle = joblib.load(model_path)
        
        # Extract components
        MODEL = bundle['model']
        FEATURE_NAMES = bundle['feature_names']
        THRESHOLD = bundle.get('threshold', 0.5)
        
        print(f"✅ Model loaded successfully")
        print(f"   Model type: {type(MODEL).__name__}")
        print(f"   Feature count: {len(FEATURE_NAMES)}")
        
        return True, "Model loaded successfully"
        
    except Exception as e:
        error_msg = f"Error loading model: {str(e)}"
        print(f"❌ {error_msg}")
        return False, error_msg

def create_simple_features(form_data):
    """Create simplified features for prediction"""
    features = {}
    
    # Main features
    main_features = [
        'cost_to_turnover', 'admin_cost_ratio', 'employment_cost_ratio',
        'financing_cost_ratio', 'deductions_to_turnover', 'high_cost_flag',
        'thin_margin_flag', 'turnover_bin_q', 'sector'
    ]
    
    for feat in main_features:
        if feat in form_data:
            if feat in ['high_cost_flag', 'thin_margin_flag']:
                features[feat] = int(form_data[feat])
            elif feat in ['cost_to_turnover', 'admin_cost_ratio', 'employment_cost_ratio', 
                         'financing_cost_ratio', 'deductions_to_turnover']:
                features[feat] = float(form_data[feat])
            else:
                features[feat] = form_data[feat]
        else:
            # Default values
            defaults = {
                'cost_to_turnover': 0.67,
                'admin_cost_ratio': 0.13,
                'employment_cost_ratio': 0.08,
                'financing_cost_ratio': 0.03,
                'deductions_to_turnover': 0.04,
                'high_cost_flag': 1,
                'thin_margin_flag': 0,
                'turnover_bin_q': 'Q3',
                'sector': 'CONSTRUCTION'
            }
            features[feat] = defaults.get(feat, '')
    
    return features

def get_risk_level(probability):
    """Determine risk level based on probability"""
    if probability >= 0.75:
        return "CRITICAL", "danger", "Immediate audit required"
    elif probability >= 0.5:
        return "HIGH", "warning", "Detailed review recommended"
    elif probability >= 0.3:
        return "MEDIUM", "info", "Monitor and review"
    else:
        return "LOW", "success", "Normal monitoring"

def calculate_risk(features):
    """Calculate risk based on features"""
    # Simple rule-based risk calculation for demo
    # Based on your notebook insights
    risk_score = 0.0
    
    # Cost to turnover is biggest factor
    cost_ratio = float(features.get('cost_to_turnover', 0.67))
    risk_score += min(cost_ratio * 0.4, 0.4)  # Up to 40%
    
    # High cost flag
    if int(features.get('high_cost_flag', 0)) == 1:
        risk_score += 0.2
    
    # Sector risk (Construction is higher risk)
    sector = features.get('sector', 'CONSTRUCTION')
    if sector == 'CONSTRUCTION':
        risk_score += 0.15
    elif sector == 'MANUFACTURING':
        risk_score += 0.10
    elif sector == 'FINANCIAL AND INSURANCE ACTIVITIES':
        risk_score -= 0.05  # Lower risk
    
    # Size risk (smaller firms higher risk)
    turnover_q = features.get('turnover_bin_q', 'Q3')
    if turnover_q == 'Q1':
        risk_score += 0.1
    elif turnover_q == 'Q2':
        risk_score += 0.05
    
    # Ensure between 0 and 1
    risk_score = max(0.0, min(risk_score, 0.95))
    
    return risk_score

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Handle single prediction requests"""
    if request.method == 'GET':
        return render_template('predict.html')
    
    elif request.method == 'POST':
        try:
            # Check if model is loaded
            if MODEL is None:
                success, message = load_model()
                if not success:
                    return render_template('results.html', 
                                         error=f"Model not loaded: {message}")
            
            # Get form data
            form_data = request.form.to_dict()
            
            # Create features
            features = create_simple_features(form_data)
            
            # Calculate risk
            probability = calculate_risk(features)
            
            # Get risk level
            risk_level, risk_color, action = get_risk_level(probability)
            
            # Prepare results
            results = {
                'probability': round(probability * 100, 2),
                'raw_probability': round(probability, 4),
                'risk_level': risk_level,
                'risk_color': risk_color,
                'action': action,
                'threshold': round(THRESHOLD * 100, 2),
                'is_high_risk': probability >= THRESHOLD,
                'features': features,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            return render_template('results.html', results=results)
            
        except Exception as e:
            error_msg = f"Prediction error: {str(e)}"
            print(f"❌ {error_msg}")
            return render_template('results.html', error=error_msg)

@app.route('/batch', methods=['GET', 'POST'])
def batch():
    """Batch processing page"""
    if request.method == 'GET':
        return render_template('batch.html')
    
    elif request.method == 'POST':
        try:
            # Check if file was uploaded
            if 'file' not in request.files:
                return render_template('batch_results.html', 
                                     error="No file uploaded")
            
            file = request.files['file']
            
            if file.filename == '':
                return render_template('batch_results.html', 
                                     error="No file selected")
            
            # Read CSV
            stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.reader(stream)
            
            # Process rows
            predictions = []
            for idx, row in enumerate(csv_input):
                if idx == 0:  # Skip header
                    continue
                    
                if len(row) >= 10:  # Check we have enough columns
                    try:
                        # Create feature dict from CSV row
                        features = {
                            'cost_to_turnover': float(row[0]),
                            'admin_cost_ratio': float(row[1]),
                            'employment_cost_ratio': float(row[2]),
                            'financing_cost_ratio': float(row[3]),
                            'deductions_to_turnover': float(row[4]),
                            'high_cost_flag': int(row[5]),
                            'thin_margin_flag': int(row[6]),
                            'turnover_bin_q': row[7],
                            'sector': row[8]
                        }
                        
                        # Calculate risk
                        probability = calculate_risk(features)
                        risk_level, _, _ = get_risk_level(probability)
                        
                        predictions.append({
                            'id': idx,
                            'probability': round(probability * 100, 2),
                            'risk_level': risk_level,
                            'is_high_risk': probability >= THRESHOLD,
                            'features': features
                        })
                    except:
                        predictions.append({
                            'id': idx,
                            'error': 'Invalid row format'
                        })
            
            # Count statistics
            high_risk_count = sum(1 for p in predictions if 'error' not in p and p['is_high_risk'])
            total_count = len(predictions)
            
            return render_template('batch_results.html', 
                                 predictions=predictions,
                                 total_count=total_count,
                                 high_risk_count=high_risk_count,
                                 threshold=THRESHOLD)
            
        except Exception as e:
            error_msg = f"Batch processing error: {str(e)}"
            print(f"❌ {error_msg}")
            return render_template('batch_results.html', error=error_msg)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        data = request.json
        
        # Create features
        features = create_simple_features(data)
        
        # Calculate risk
        probability = calculate_risk(features)
        
        # Get risk level
        risk_level, _, action = get_risk_level(probability)
        
        return jsonify({
            'success': True,
            'probability': float(probability),
            'risk_level': risk_level,
            'action': action,
            'is_high_risk': probability >= THRESHOLD,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    if MODEL is not None:
        return jsonify({'status': 'healthy', 'model_loaded': True})
    else:
        return jsonify({'status': 'loading', 'model_loaded': False})

@app.route('/model-info')
def model_info():
    """Get model information"""
    if MODEL is None:
        return jsonify({'error': 'Model not loaded'}), 404
    
    return jsonify({
        'model_type': type(MODEL).__name__,
        'feature_count': len(FEATURE_NAMES) if FEATURE_NAMES else 0,
        'threshold': THRESHOLD,
        'loaded': True
    })

# Load model when app starts
print("🚀 Starting CIT Loss Prediction System (Complete Version)...")
load_model()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
