"""
CIT Loss Prediction System - Main Application
Version: 2.0.0
Production Ready Flask Web Application
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import pickle
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.prediction.predictor import Predictor
from src.utils.logger import setup_logger

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize components
logger = setup_logger()
predictor = Predictor()

@app.route('/')
def index():
    """Main dashboard"""
    return render_template('index.html')

@app.route('/cit/batch')
def cit_batch():
    """Batch processing interface"""
    return render_template('cit_batch.html')

@app.route('/api/predict', methods=['POST'])
def predict_single():
    """Single prediction API"""
    try:
        data = request.get_json()
        prediction = predictor.predict_single(data)
        return jsonify(prediction)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'model_loaded': predictor.model_loaded
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
