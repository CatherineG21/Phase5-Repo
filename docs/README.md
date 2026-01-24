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

## 🚀 Web Application Deployment

A complete Flask web application is included for interactive risk assessment.

### Quick Access Links
- **Live Application**: [http://localhost:5000](http://localhost:5000) (when running locally)
- **Source Code**: [app.py](https://raw.githubusercontent.com/CatherineG21/Phase5-Repo/master/app.py)
- **API Health Check**: [http://localhost:5000/health](http://localhost:5000/health)
- **Model Information**: [http://localhost:5000/model-info](http://localhost:5000/model-info)

### Features
- **Single Firm Assessment**: Form-based risk scoring
- **Batch Processing**: Upload CSV files for bulk analysis
- **REST API**: JSON endpoints for system integration
- **Professional Interface**: KRA-branded web interface

### Quick Deployment
```bash
# 1. Clone repository
git clone https://github.com/CatherineG21/Phase5-Repo.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add model file (download separately)
# Place in: deployment_artifacts/kra_cit_risk_model_v1.pkl

# 4. Run application
python app.py

# 5. Access at: http://localhost:5000


## 🚀 Web Application Deployment

A complete Flask web application is included for interactive risk assessment.

### Quick Access
- **Live App**: http://localhost:5000
- **Source**: https://raw.githubusercontent.com/CatherineG21/Phase5-Repo/master/app.py
- **Health**: http://localhost:5000/health
- **Model Info**: http://localhost:5000/model-info

### Quick Start
```bash
git clone https://github.com/CatherineG21/Phase5-Repo.git
pip install -r requirements.txt
python app.py

