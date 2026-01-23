import joblib
import os

# Check if model file exists
model_path = "deployment_artifacts/kra_cit_risk_model_v1.pkl"
if not os.path.exists(model_path):
    model_path = "Models/kra_cit_risk_model_v1.pkl"
    print(f"Trying alternative path: {model_path}")

if os.path.exists(model_path):
    print(f"✅ Model found at: {model_path}")
    
    # Load the model
    try:
        bundle = joblib.load(model_path)
        print("\n✅ Model loaded successfully!")
        print(f"Bundle type: {type(bundle)}")
        
        # Check what's in the bundle
        print("\n📦 Bundle contents:")
        for key in bundle.keys():
            print(f"  - {key}: {type(bundle[key])}")
            
        # If it's a dict, show more details
        if isinstance(bundle, dict):
            print("\n🔍 Detailed inspection:")
            for key, value in bundle.items():
                print(f"\n{key}:")
                if hasattr(value, '__class__'):
                    print(f"  Type: {value.__class__.__name__}")
                if hasattr(value, 'shape'):
                    print(f"  Shape: {value.shape}")
                if isinstance(value, list):
                    print(f"  Length: {len(value)}")
                    if len(value) > 0:
                        print(f"  First item: {value[0]}")
        
    except Exception as e:
        print(f"❌ Error loading model: {e}")
else:
    print(f"❌ Model not found at either location")
