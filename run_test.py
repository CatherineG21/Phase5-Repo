#!/usr/bin/env python3
"""
Test the Flask application
"""
import sys
import os
import subprocess
import time
import requests

print("🚀 Testing CIT Loss Prediction System...")

# Check if app.py exists
if not os.path.exists("app.py"):
    print("❌ app.py not found!")
    sys.exit(1)

print("✅ app.py found")

# Check if templates exist
required_templates = ["base.html", "index.html", "predict.html", "results.html", "batch.html", "batch_results.html"]
missing_templates = []

for template in required_templates:
    path = os.path.join("templates", template)
    if not os.path.exists(path):
        missing_templates.append(template)

if missing_templates:
    print(f"❌ Missing templates: {missing_templates}")
else:
    print("✅ All templates found")

# Test model loading
try:
    from app import load_model
    success, message = load_model()
    if success:
        print(f"✅ Model loading: {message}")
    else:
        print(f"❌ Model loading failed: {message}")
except Exception as e:
    print(f"❌ Error importing app: {e}")

print("\n🎉 Basic structure verification complete!")
print("\nTo run the application:")
print("1. Make sure you're in the project directory")
print("2. Run: python app.py")
print("3. Open browser and go to: http://localhost:5000")
print("4. Press Ctrl+C to stop the server")
