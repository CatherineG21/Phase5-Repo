# CIT Loss Prediction for Kenya Revenue Authority

## Project Overview
This project predicts loss-making firms from Corporate Income Tax (CIT) returns to help KRA improve audit targeting and revenue recovery.

## Key Results
- XGBoost model achieves 85.4% ROC-AUC
- Identifies high-risk loss-making firms with 81.7% precision
- Potential KES 50M+ annual revenue recovery

## Project Structure
-  - Jupyter notebook with full analysis
-  - Source code for preprocessing, modeling, inference
-  - Production scoring engine
-  - Sample data files
-  - Trained model (gitignored, download instructions in README)
-  - Unit tests
-  - Documentation

## Quick Start
1. Install requirements: `pip install -r requirements.txt`
2. Run scoring: `python Deployment/score_firms.py`

## Deployment
See `docs/deployment.md` for production deployment instructions.
