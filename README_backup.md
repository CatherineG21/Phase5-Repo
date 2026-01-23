# CIT Loss Prediction Dashboard - Kenya Revenue Authority

## 🚀 Complete Web Dashboard v2.0
A comprehensive Flask-based dashboard for CIT risk assessment and management.

## ✨ NEW in Version 2.0: CIT Batch Processing
**Bulk analysis of multiple CIT returns via CSV/Excel upload**

**Features Added:**
- Batch upload with drag & drop interface
- File validation for required columns: PIN_NO, BUSINESS_SUBTYPE, GROSS_TURNOVER
- File preview before processing
- Batch risk assessment for hundreds of records
- Download results as CSV
- Template download system

**Access:** \`http://localhost:5000/cit/batch\`

## 📊 Complete Dashboard Features

### 1. **Dashboard Home** (\`/\`)
- System overview and quick access
- Feature cards with descriptions
- Navigation to all tools

### 2. **CIT Batch Processing** (\`/cit/batch\`) - **NEW**
- Upload multiple CIT returns (CSV/Excel)
- Bulk risk assessment
- Export results as CSV
- Template download

### 3. **Risk Calculator** (\`/predict\`)
- Individual taxpayer risk assessment
- Ratio-based risk scoring
- Real-time calculations
- Detailed risk reports

### 4. **Raw Data Input** (\`/raw_input\`)
- Direct CIT data entry forms
- Comprehensive field input
- Immediate risk scoring
- Data validation

### 5. **Audit Management** (\`/audit-list\`)
- Audit case listing
- Case status tracking
- Priority assignment
- Management tools

### 6. **Monitoring** (\`/monitoring\`)
- System performance tracking
- User activity monitoring
- Data quality checks
- Alert system

### 7. **Batch Tools** (\`/batch\`)
- Additional batch operations
- Data processing utilities
- Report generation
- Export functionalities

### 8. **Results & Analysis** (\`/results\`)
- Detailed analysis views
- Historical data
- Trend analysis
- Export options

## Project Overview
This project develops a machine learning system to predict loss-making firms from Corporate Income Tax (CIT) returns. The solution helps the Kenya Revenue Authority (KRA) improve audit targeting efficiency and maximize revenue recovery through data-driven risk assessment.

## Key Results
- **Model Performance**: XGBoost classifier achieves 85.4% ROC-AUC
- **Precision**: Identifies high-risk loss-making firms with 81.7% precision
- **Revenue Impact**: Projects potential recovery of KES 50M+ annually
- **Efficiency Gain**: Reduces manual review workload by ~70%
- **Batch Processing**: Handle 100+ CIT returns in single upload

## Project Structure
\`\`\`
Phase5-Repo/
├── notebooks/              # Jupyter notebooks with full analysis
├── src/                   # Source code modules
│   ├── preprocessing/     # Data cleaning and feature engineering
│   ├── modeling/         # Model training and evaluation
│   └── inference/        # Production scoring engine
├── app/                   # Flask Dashboard Application
│   ├── app.py            # Main dashboard with ALL features
│   └── templates/        # Complete HTML template system
│       ├── index.html           # Dashboard home
│       ├── cit_batch.html       # CIT batch upload (NEW)
│       ├── cit_preview.html     # File preview
│       ├── cit_results.html     # Batch results
│       ├── predict.html         # Risk calculator
│       ├── raw_input.html       # Raw data input
│       ├── audit_list.html      # Audit management
│       ├── monitoring.html      # System monitoring
│       ├── batch.html           # Batch tools
│       ├── results.html         # Analysis results
│       └── base.html            # Base template with navigation
├── data/
│   ├── sample/           # Sample data files
│   └── processed/        # Processed datasets
├── models/               # Trained models (.gitignored)
├── tests/                # Unit tests
├── docs/                 # Documentation
├── requirements.txt      # Python dependencies
└── README.md            # This file
\`\`\`

## Quick Start
\`\`\`bash
# Install dependencies
pip install -r requirements.txt

# Start the dashboard
python app.py

# Open browser to: http://localhost:5000
\`\`\`

## Dashboard Access Points
| Feature | Description | Access |
|---------|-------------|--------|
| **Dashboard Home** | Main system overview | \`http://localhost:5000\` |
| **CIT Batch Processing** | Bulk CIT return upload | \`http://localhost:5000/cit/batch\` |
| **Risk Calculator** | Individual risk assessment | \`http://localhost:5000/predict\` |
| **Raw Data Input** | Direct CIT data entry | \`http://localhost:5000/raw_input\` |
| **Audit Management** | Case tracking | \`http://localhost:5000/audit-list\` |
| **System Monitoring** | Performance tracking | \`http://localhost:5000/monitoring\` |
| **Batch Tools** | Additional utilities | \`http://localhost:5000/batch\` |
| **Results Analysis** | Detailed views | \`http://localhost:5000/results\` |

## CIT Batch Processing Workflow
1. Navigate to: \`http://localhost:5000/cit/batch\`
2. Upload CSV/Excel file with CIT data
3. Required columns: PIN_NO, BUSINESS_SUBTYPE, GROSS_TURNOVER
4. Preview first 5 records
5. Click "Process All Records"
6. View results and download CSV

## Distributable Package
A standalone package \`CIT_Loss_Prediction_System.zip\` is included for easy distribution.

## Support
For issues with any dashboard feature, check the specific documentation.

---
**Last Updated**: January 2025  
**Version**: 2.0.0 (Complete Dashboard with CIT Batch Processing)  
**System Type**: Complete Flask Web Dashboard
