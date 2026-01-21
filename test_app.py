#!/usr/bin/env python3
"""
Quick test to verify Flask app structure
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, load_model
    
    print("✅ Flask app imported successfully")
    
    # Test model loading
    success, message = load_model()
    if success:
        print(f"✅ Model loading test: {message}")
    else:
        print(f"❌ Model loading test failed: {message}")
        
    # Check if app has required routes
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule))
    
    print(f"\n📋 Available routes:")
    for route in sorted(routes):
        print(f"  - {route}")
    
    print("\n🎉 App structure looks good!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
