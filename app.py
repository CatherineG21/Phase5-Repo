from flask import Flask, render_template, request, flash, redirect, jsonify, session, send_file
from datetime import datetime
import os
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = 'cit-2024-key'

print("=" * 60)
print("CIT LOSS PREDICTION SYSTEM - WITH BATCH PROCESSING")
print("=" * 60)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """Ratio input - SIMPLE WORKING VERSION"""
    print(f"PREDICT route called. Method: {request.method}")

    if request.method == 'GET':
        return render_template('predict_fixed.html')

    elif request.method == 'POST':
        print("PREDICT form submitted!")
        print(f"Form data: {dict(request.form)}")

        try:
            cost_ratio = float(request.form.get('cost_to_turnover', 0))
            finance_ratio = float(request.form.get('financing_cost_ratio', 0))

            print(f"Cost ratio: {cost_ratio}, Finance ratio: {finance_ratio}")

            risk_score = 30

            if cost_ratio > 0.8:
                risk_score += 40
            elif cost_ratio > 0.6:
                risk_score += 25
            elif cost_ratio > 0.4:
                risk_score += 15

            if finance_ratio > 0.3:
                risk_score += 30
            elif finance_ratio > 0.2:
                risk_score += 20
            elif finance_ratio > 0.1:
                risk_score += 10

            risk_score = min(risk_score, 100)

            print(f"Risk calculated: {risk_score}%")

            return f'''
            <!DOCTYPE html>
            <html>
            <body style="padding: 20px; font-family: Arial;">
                <h1>Risk Assessment Complete</h1>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                    <h2 style="color: blue;">Risk Score: {risk_score}%</h2>
                    <p><strong>Risk Level:</strong> {'HIGH' if risk_score > 50 else 'MEDIUM' if risk_score > 30 else 'LOW'}</p>
                    <p><strong>Action:</strong> {'Review needed' if risk_score > 50 else 'Monitor'}</p>
                    <p><strong>Time:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
                </div>
                <br>
                <a href="/predict" style="padding: 10px 20px; background: blue; color: white; text-decoration: none;">Back to Calculator</a>
            </body>
            </html>
            '''

        except Exception as e:
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return f"<h1>Error</h1><p>{str(e)}</p><a href='/predict'>Back</a>"

@app.route('/raw_input')
def raw_input_form():
    return render_template('raw_input.html')

@app.route('/predict_raw', methods=['POST'])
def predict_raw():
    """Process raw CIT data"""
    print("RAW CIT data submitted!")
    print(f"Data: {dict(request.form)}")

    try:
        turnover = float(request.form.get('GROSS_TURNOVER', 0))
        direct_costs = float(request.form.get('ODC_TOT_OF_OTHER_DIRECT_COSTS', 0))
        interest = float(request.form.get('FINCEXP_INTEREST_EXP', 0))

        cost_ratio = direct_costs / turnover if turnover > 0 else 0
        finance_ratio = interest / turnover if turnover > 0 else 0

        risk_score = 30
        if cost_ratio > 0.8: risk_score += 40
        elif cost_ratio > 0.6: risk_score += 25
        elif cost_ratio > 0.4: risk_score += 15

        if finance_ratio > 0.3: risk_score += 30
        elif finance_ratio > 0.2: risk_score += 20
        elif finance_ratio > 0.1: risk_score += 10

        risk_score = min(risk_score, 100)

        return f'''
        <!DOCTYPE html>
        <html>
        <body style="padding: 30px; font-family: Arial;">
            <h1>Raw CIT Data Analysis Results</h1>
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                <h2 style="color: {'red' if risk_score > 50 else 'orange' if risk_score > 30 else 'green'}">
                    Risk Score: {risk_score}%
                </h2>
                <p><strong>PIN:</strong> {request.form.get('PIN_NO', 'N/A')}</p>
                <p><strong>Sector:</strong> {request.form.get('BUSINESS_SUBTYPE', 'N/A')}</p>
                <p><strong>Turnover:</strong> KES {turnover:,.2f}</p>
                <p><strong>Cost Ratio:</strong> {cost_ratio:.2%}</p>
                <p><strong>Finance Ratio:</strong> {finance_ratio:.2%}</p>
                <p><strong>Time:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>
            <br>
            <a href="/raw_input" style="padding: 10px 20px; background: blue; color: white; text-decoration: none; margin-right: 10px;">
                Back to Raw Input
            </a>
            <a href="/" style="padding: 10px 20px; background: green; color: white; text-decoration: none;">
                Go to Dashboard
            </a>
        </body>
        </html>
        '''

    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

@app.route('/batch')
def batch():
    return render_template('batch.html')

@app.route('/audit-list')
def audit_list():
    return render_template('audit_list.html')

# ============================================================================
# CIT BATCH PROCESSING ROUTES
# ============================================================================

@app.route('/cit/batch')
def cit_batch():
    """CIT Batch Processing Upload Page"""
    return render_template('cit_batch.html')

@app.route('/cit/upload', methods=['POST'])
def cit_upload():
    """Handle CIT file upload"""
    try:
        if 'cit_file' not in request.files:
            flash('No file selected', 'danger')
            return redirect(url_for('cit_batch'))
        
        file = request.files['cit_file']
        
        if file.filename == '':
            flash('No file selected', 'danger')
            return redirect(url_for('cit_batch'))
        
        allowed_extensions = {'csv', 'xlsx'}
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_ext not in allowed_extensions:
            flash('Only CSV and Excel files are allowed', 'danger')
            return redirect(url_for('cit_batch'))
        
        upload_dir = 'uploads'
        os.makedirs(upload_dir, exist_ok=True)
        
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(upload_dir, unique_filename)
        file.save(filepath)
        
        if file_ext == 'csv':
            df = pd.read_csv(filepath, encoding='utf-8')
        else:
            df = pd.read_excel(filepath)
        
        required_columns = ['PIN_NO', 'BUSINESS_SUBTYPE', 'GROSS_TURNOVER']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            os.remove(filepath)
            flash(f'Missing required columns: {", ".join(missing_columns)}', 'danger')
            return redirect(url_for('cit_batch'))
        
        session['cit_batch_file'] = {
            'filename': filename,
            'filepath': filepath,
            'records': len(df),
            'columns': list(df.columns),
            'sample': df.head(5).to_dict('records')
        }
        
        flash(f'✅ File uploaded successfully! Found {len(df)} records.', 'success')
        return redirect(url_for('cit_preview'))
        
    except Exception as e:
        flash(f'Error uploading file: {str(e)}', 'danger')
        return redirect(url_for('cit_batch'))

@app.route('/cit/preview')
def cit_preview():
    """Preview uploaded CIT data"""
    if 'cit_batch_file' not in session:
        flash('Please upload a file first', 'warning')
        return redirect(url_for('cit_batch'))
    
    file_info = session['cit_batch_file']
    
    return render_template('cit_preview.html', 
                         filename=file_info['filename'],
                         records=file_info['records'],
                         columns=file_info['columns'],
                         sample_data=file_info['sample'])

@app.route('/cit/process', methods=['POST'])
def cit_process():
    """Process the CIT batch file"""
    if 'cit_batch_file' not in session:
        return jsonify({'success': False, 'message': 'No file uploaded'})
    
    file_info = session['cit_batch_file']
    
    try:
        if file_info['filename'].endswith('.csv'):
            df = pd.read_csv(file_info['filepath'], encoding='utf-8')
        else:
            df = pd.read_excel(file_info['filepath'])
        
        results = []
        
        for _, row in df.iterrows():
            turnover = float(row.get('GROSS_TURNOVER', 0))
            direct_costs = float(row.get('ODC_TOT_OF_OTHER_DIRECT_COSTS', 0))
            interest = float(row.get('FINCEXP_INTEREST_EXP', 0))
            
            cost_ratio = direct_costs / turnover if turnover > 0 else 0
            finance_ratio = interest / turnover if turnover > 0 else 0
            
            risk_score = 30
            if cost_ratio > 0.8: risk_score += 40
            elif cost_ratio > 0.6: risk_score += 25
            elif cost_ratio > 0.4: risk_score += 15

            if finance_ratio > 0.3: risk_score += 30
            elif finance_ratio > 0.2: risk_score += 20
            elif finance_ratio > 0.1: risk_score += 10

            risk_score = min(risk_score, 100)
            
            if risk_score > 50:
                risk_level = 'HIGH'
                risk_color = 'danger'
            elif risk_score > 30:
                risk_level = 'MEDIUM'
                risk_color = 'warning'
            else:
                risk_level = 'LOW'
                risk_color = 'success'
            
            results.append({
                'PIN_NO': str(row.get('PIN_NO', 'N/A')),
                'BUSINESS_SUBTYPE': str(row.get('BUSINESS_SUBTYPE', 'N/A')),
                'GROSS_TURNOVER': f"{turnover:,.2f}",
                'COST_RATIO': f"{cost_ratio:.2%}",
                'FINANCE_RATIO': f"{finance_ratio:.2%}",
                'RISK_SCORE': f"{risk_score}%",
                'RISK_LEVEL': risk_level,
                'RISK_COLOR': risk_color,
                'ACTION': 'Review needed' if risk_score > 50 else 'Monitor'
            })
        
        results_df = pd.DataFrame(results)
        output_filename = f"cit_results_{uuid.uuid4().hex[:8]}.csv"
        output_path = os.path.join('uploads', output_filename)
        results_df.to_csv(output_path, index=False)
        
        session['cit_results'] = {
            'output_file': output_filename,
            'total_records': len(results),
            'high_risk': len([r for r in results if r['RISK_LEVEL'] == 'HIGH']),
            'medium_risk': len([r for r in results if r['RISK_LEVEL'] == 'MEDIUM']),
            'low_risk': len([r for r in results if r['RISK_LEVEL'] == 'LOW'])
        }
        
        if os.path.exists(file_info['filepath']):
            os.remove(file_info['filepath'])
        session.pop('cit_batch_file', None)
        
        return jsonify({
            'success': True,
            'message': f'Successfully processed {len(results)} records',
            'high_risk': session['cit_results']['high_risk'],
            'medium_risk': session['cit_results']['medium_risk'],
            'low_risk': session['cit_results']['low_risk']
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Processing error: {str(e)}'})

@app.route('/cit/results')
def cit_results():
    """Show CIT batch processing results"""
    if 'cit_results' not in session:
        flash('No results found. Please process a batch first.', 'warning')
        return redirect(url_for('cit_batch'))
    
    results_info = session['cit_results']
    
    results_path = os.path.join('uploads', results_info['output_file'])
    if os.path.exists(results_path):
        df = pd.read_csv(results_path)
        results_table = df.to_dict('records')
    else:
        results_table = []
    
    return render_template('cit_results.html',
                         results_table=results_table,
                         total_records=results_info['total_records'],
                         high_risk=results_info['high_risk'],
                         medium_risk=results_info['medium_risk'],
                         low_risk=results_info['low_risk'])

@app.route('/cit/download')
def cit_download():
    """Download processed results"""
    if 'cit_results' not in session:
        flash('No results to download', 'warning')
        return redirect(url_for('cit_batch'))
    
    results_file = session['cit_results']['output_file']
    filepath = os.path.join('uploads', results_file)
    
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        flash('Results file not found', 'danger')
        return redirect(url_for('cit_batch'))

@app.route('/cit/template')
def cit_template():
    """Download CIT template"""
    template_data = {
        'PIN_NO': ['A123456789X', 'B987654321Y', 'C112233445Z'],
        'BUSINESS_SUBTYPE': ['Manufacturing', 'Services', 'Retail'],
        'GROSS_TURNOVER': [25000000, 15000000, 8000000],
        'ODC_TOT_OF_OTHER_DIRECT_COSTS': [20000000, 12000000, 7000000],
        'FINCEXP_INTEREST_EXP': [750000, 300000, 160000],
        'TAX_YEAR': [2023, 2023, 2023]
    }
    
    df = pd.DataFrame(template_data)
    template_path = os.path.join('uploads', 'cit_template.csv')
    df.to_csv(template_path, index=False)
    
    return send_file(template_path, 
                    as_attachment=True, 
                    download_name='cit_batch_template.csv')

if __name__ == '__main__':
    print("✅ Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"   {rule.rule} -> {rule.endpoint}")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
