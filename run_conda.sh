#!/bin/bash
echo "========================================"
echo "   CIT LOSS PREDICTION SYSTEM"
echo "========================================"
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "WARNING: Conda not found!"
    echo ""
    echo "Please run this from your Anaconda terminal or"
    echo "activate your environment first."
    echo ""
    echo "For Anaconda users:"
    echo "1. Open Anaconda Prompt/Terminal"
    echo "2. Navigate to this folder"
    echo "3. Run: python app.py"
    echo ""
    exit 1
fi

echo "Checking dependencies..."
pip install -r requirements_simple.txt

echo ""
echo "========================================"
echo "STARTING CIT SYSTEM..."
echo "========================================"
echo ""
echo "Open your browser and visit:"
echo "    http://localhost:5000"
echo ""
echo "To stop, press: Ctrl+C"
echo ""
echo "========================================"
python app.py
