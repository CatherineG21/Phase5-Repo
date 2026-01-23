#!/bin/bash

echo "Reorganizing CIT Loss Prediction System..."

# Create new directory structure
mkdir -p src/models src/preprocessing src/prediction src/utils
mkdir -p app/static/css app/static/js app/static/images
mkdir -p data/raw data/processed data/sample
mkdir -p tests/test_data
mkdir -p deployment/nginx

# Move source files to src/
if [ -d "Models/" ]; then
    mv Models/* models/ 2>/dev/null || true
    rmdir Models/ 2>/dev/null || true
fi

# Move app files
if [ -d "templates/" ]; then
    mv templates/* app/templates/ 2>/dev/null || true
    rmdir templates/ 2>/dev/null || true
fi

if [ -d "templates_backup/" ]; then
    mv templates_backup/* app/templates/ 2>/dev/null || true
    rmdir templates_backup/ 2>/dev/null || true
fi

if [ -d "static/" ]; then
    mv static/* app/static/ 2>/dev/null || true
    rmdir static/ 2>/dev/null || true
fi

# Move data files
if [ -d "Data/" ]; then
    mv Data/* data/ 2>/dev/null || true
    rmdir Data/ 2>/dev/null || true
fi

# Move test files
if [ -d "test_data/" ]; then
    mv test_data/* tests/test_data/ 2>/dev/null || true
    rmdir test_data/ 2>/dev/null || true
fi

# Move deployment files
if [ -d "Deployment/" ]; then
    mv Deployment/* deployment/ 2>/dev/null || true
    rmdir Deployment/ 2>/dev/null || true
fi

# Move documentation
if [ -d "docs/" ]; then
    mkdir -p docs/old
    mv docs/* docs/old/ 2>/dev/null || true
fi

# Create __init__.py files
touch src/__init__.py
touch src/models/__init__.py
touch src/preprocessing/__init__.py
touch src/prediction/__init__.py
touch src/utils/__init__.py
touch app/__init__.py
touch tests/__init__.py

# Update app.py imports (we'll need to modify this)
echo "Creating new app.py structure..."

# Create a clean app.py with proper imports
cat > app.py << 'PYTHON'
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
PYTHON

# Create minimal src files
cat > src/prediction/predictor.py << 'PYTHON'
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
PYTHON

cat > src/utils/logger.py << 'PYTHON'
"""
Logging utilities
"""

import logging
import os
from datetime import datetime

def setup_logger(name='cit_predictor', log_dir='logs'):
    """Setup application logger"""
    os.makedirs(log_dir, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # File handler
    log_file = os.path.join(log_dir, f'{datetime.now().strftime("%Y%m%d")}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
PYTHON

echo "Creating requirements files..."

# Create proper requirements.txt
cat > requirements.txt << 'TXT'
# Core dependencies
flask==2.3.3
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
xgboost==1.7.6
joblib==1.3.2

# Web & UI
jinja2==3.1.2
wtforms==3.0.1
flask-wtf==1.1.1

# Data processing
openpyxl==3.1.2
python-dotenv==1.0.0

# Development
pytest==7.4.0
black==23.7.0
flake8==6.0.0
jupyter==1.0.0

# Production
gunicorn==20.1.0
TXT

# Keep the simple requirements
if [ -f "requirements_simple.txt" ]; then
    cp requirements_simple.txt .
fi

echo "Updating templates structure..."

# Create base template if it doesn't exist
if [ ! -f "app/templates/base.html" ]; then
    cat > app/templates/base.html << 'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIT Loss Prediction System - KRA</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <div class="nav-brand">
                <img src="{{ url_for('static', filename='images/kra_logo.png') }}" alt="KRA Logo" height="40">
                <span>CIT Loss Prediction System</span>
            </div>
            <ul class="nav-menu">
                <li><a href="{{ url_for('index') }}">Dashboard</a></li>
                <li><a href="{{ url_for('cit_batch') }}">Batch Processing</a></li>
                <li><a href="/monitoring">Monitoring</a></li>
                <li><a href="/audit">Audit List</a></li>
            </ul>
        </div>
    </nav>
    
    <main class="container">
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <div class="container">
            <p>© 2024 Kenya Revenue Authority. Version 2.0.0</p>
        </div>
    </footer>
    
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
HTML
fi

echo "Project reorganization complete!"
echo "New structure:"
find . -type f -name "*.py" -o -name "*.html" -o -name "*.md" -o -name "*.txt" | head -20
