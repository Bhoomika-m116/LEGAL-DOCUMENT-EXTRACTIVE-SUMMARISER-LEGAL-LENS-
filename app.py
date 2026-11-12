import os
import io
import json
import tempfile
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for, 
    flash, session, jsonify, send_file, abort
)
from werkzeug.utils import secure_filename

from config import Config
from database import (
    init_db, create_user, authenticate_user, get_user_by_id,
    save_summary_record, get_user_summaries, get_summary_by_id, delete_summary
)
from summarizer.nlp_preprocessor import LegalNLPPreprocessor
from summarizer.ocr_parser import DocumentParser
from summarizer.extractive_engine import HybridExtractiveSummarizer
from summarizer.report_generator import LegalReportGenerator
from comparison_engine import compare_contracts

app = Flask(__name__)
app.config.from_object(Config)

# Ensure required folders exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.REPORT_FOLDER, exist_ok=True)
os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)

# Initialize database
init_db()

# Initialize core services
parser = DocumentParser()
nlp = LegalNLPPreprocessor()
summarizer_engine = HybridExtractiveSummarizer()
report_gen = LegalReportGenerator()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session and not session.get('is_guest', False):
            flash('Please log in or proceed as a guest to access the legal dashboard.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

# Context processor for templates
@app.context_processor
def inject_user():
    return {
        'current_user': session.get('username', None),
        'is_guest': session.get('is_guest', False),
        'user_full_name': session.get('full_name', 'Guest User'),
        'current_year': datetime.now().year
    }

# ----------------- ROUTES ----------------- #

@app.route('/')
def index():
    """Official portal homepage with animated legal graphics and showcase."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')
        
        user = authenticate_user(identifier, password)
        if user:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name'] or user['username']
            session['is_guest'] = False
            flash(f"Welcome back, {session['full_name']}!", 'success')
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid legal credential or password. Please verify.", "danger")
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        organization = request.form.get('organization', '').strip()

        if len(username) < 3:
            flash("Username must be at least 3 characters.", "danger")
            return render_template('register.html')
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template('register.html')

        success, res = create_user(username, email, password, full_name, organization)
        if success:
            flash("Legal practitioner account successfully registered. Please log in.", "success")
            return redirect(url_for('login'))
        else:
            flash(f"Registration failed: {res}", "danger")

    return render_template('register.html')

@app.route('/guest')
def guest_mode():
    """Enables instant Guest Mode access without credentials."""
    session.clear()
    session['user_id'] = None
    session['username'] = 'Guest Counsel'
    session['full_name'] = 'Guest Practitioner'
    session['is_guest'] = True
    flash("Browsing in Official Guest Mode. All legal analytics features are active.", "info")
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash("You have successfully signed out of the Legal Portal.", "info")
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Main legal document summarization workroom."""
    return render_template('dashboard.html')

@app.route('/analyze', methods=['POST'])
@login_required
def analyze_document():
    """Performs full OCR/extraction, NLP preprocessing, and extractive summarization."""
    raw_text = ""
    filename = "Pasted_Legal_Instrument.txt"
    doc_type = "Direct Text Input"
    method_used = "Manual Input"
    page_count = 1

    ratio = float(request.form.get('summary_ratio', Config.DEFAULT_SUMMARY_RATIO))
    algorithm = request.form.get('algorithm', 'hybrid')
    force_ocr = request.form.get('force_ocr') == 'on'

    # Check for file upload
    if 'document_file' in request.files and request.files['document_file'].filename:
        file = request.files['document_file']
        if allowed_file(file.filename):
            sec_name = secure_filename(file.filename)
            filename = sec_name
            save_path = os.path.join(Config.UPLOAD_FOLDER, sec_name)
            file.save(save_path)
            
            # Determine format
            ext = sec_name.rsplit('.', 1)[1].lower()
            if ext == 'pdf':
                doc_type = "PDF Legal Brief"
            elif ext == 'docx':
                doc_type = "Word Legal Contract"
            elif ext in ['png', 'jpg', 'jpeg', 'tiff', 'bmp']:
                doc_type = "Scanned Legal Affidavit / Image"
            else:
                doc_type = "Legal Text Document"

            try:
                raw_text, method_used, page_count = parser.parse_file(save_path, force_ocr=force_ocr)
            except Exception as e:
                flash(f"Error reading legal file: {str(e)}", "danger")
                return redirect(url_for('dashboard'))
        else:
            flash("Unsupported file extension. Allowed: PDF, DOCX, TXT, PNG, JPG.", "danger")
            return redirect(url_for('dashboard'))
    else:
        # Check pasted text
        raw_text = request.form.get('document_text', '').strip()
        if not raw_text:
            flash("Please either upload a document file or paste legal text to proceed.", "warning")
            return redirect(url_for('dashboard'))

    if len(raw_text.strip()) < 50:
        flash("The document contains insufficient readable text for extractive analysis.", "danger")
        return redirect(url_for('dashboard'))

    # Run Extractive Summarizer
    results = summarizer_engine.summarize(raw_text, ratio=ratio, algorithm=algorithm)
    results['filename'] = filename
    results['doc_type'] = doc_type
    results['method_used'] = method_used
    results['page_count'] = page_count
    results['algorithm_used'] = algorithm.capitalize()

    # Save to history database (supports both registered users and guest sessions)
    user_id = session.get('user_id')
    record_id = save_summary_record(
        user_id=user_id,
        filename=filename,
        doc_type=doc_type,
        orig_words=results['original_words'],
        sum_words=results['summary_words'],
        accuracy=results['accuracy_score'],
        compression=results['compression_ratio'],
        risk_level=results['risk_analysis'].get('level', 'Low'),
        risk_score=results['risk_analysis'].get('score', 0),
        clauses=results['clauses'],
        legalese=results['legalese'],
        summary_text=results['summary_text'],
        preview_text=raw_text
    )
    results['record_id'] = record_id

    # Store current result in session for quick re-export
    session['last_summary'] = results

    return render_template('result.html', result=results)

@app.route('/summary/<int:summary_id>')
@login_required
def view_summary(summary_id):
    """Retrieves an archived legal summary by ID."""
    rec = get_summary_by_id(summary_id)
    if not rec:
        flash("Summary record not found or inaccessible.", "danger")
        return redirect(url_for('history'))

    # Reconstruct result structure
    result = {
        'record_id': rec['id'],
        'filename': rec['filename'],
        'doc_type': rec['doc_type'],
        'method_used': 'Archived Database Record',
        'original_words': rec['original_words'],
        'summary_words': rec['summary_words'],
        'accuracy_score': rec['accuracy_score'],
        'compression_ratio': rec['compression_ratio'],
        'time_saved_minutes': max(1, int(round((rec['original_words'] - rec['summary_words']) / 200))),
        'summary_text': rec['summary_text'],
        'summary_sentences': [s.strip() for s in rec['summary_text'].split('. ') if s.strip()],
        'clauses': rec['clauses'],
        'legalese': rec['legalese'],
        'risk_analysis': {
            'level': rec['risk_level'],
            'score': rec['risk_score'],
            'safety_index': 100 - rec['risk_score'],
            'flags': []
        },
        'readability_summary': {'difficulty': 'Extracted Legal Precision', 'grade_level': 12.0}
    }
    return render_template('result.html', result=result)

@app.route('/download-pdf/<int:summary_id>')
@login_required
def download_summary_pdf(summary_id):
    """Generates and streams an official PDF summary brief."""
    rec = get_summary_by_id(summary_id)
    if not rec:
        abort(404)

    summary_data = {
        'filename': rec['filename'],
        'original_words': rec['original_words'],
        'summary_words': rec['summary_words'],
        'accuracy_score': rec['accuracy_score'],
        'compression_ratio': rec['compression_ratio'],
        'summary_text': rec['summary_text'],
        'summary_sentences': [s.strip() for s in rec['summary_text'].split('. ') if s.strip()],
        'clauses': rec['clauses'],
        'legalese': rec['legalese'],
        'risk_analysis': {'level': rec['risk_level'], 'score': rec['risk_score']}
    }

    base_name = os.path.splitext(rec['filename'])[0]
    pdf_path = report_gen.generate_pdf(base_name, rec['filename'], summary_data)
    
    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=f"Official_Legal_Summary_{base_name}.pdf",
        mimetype='application/pdf'
    )

@app.route('/history')
@login_required
def history():
    """Lists audit trail of processed legal instruments."""
    user_id = session.get('user_id')
    summaries = get_user_summaries(user_id)
    return render_template('history.html', summaries=summaries)

@app.route('/delete-summary/<int:summary_id>', methods=['POST'])
@login_required
def delete_summary_route(summary_id):
    user_id = session.get('user_id')
    delete_summary(summary_id, user_id=user_id)
    flash("Record successfully expunged from history ledger.", "info")
    return redirect(url_for('history'))

@app.route('/compare', methods=['GET', 'POST'])
@login_required
def compare_documents():
    """Compare two legal instruments supplied as pasted text or uploaded files."""
    comparison_result = None
    doc1_text = ''
    doc2_text = ''
    doc1_source = 'Pasted text'
    doc2_source = 'Pasted text'

    if request.method == 'POST':
        doc1_text = request.form.get('doc1_text', '').strip()
        doc2_text = request.form.get('doc2_text', '').strip()

        # Each instrument can independently be pasted or uploaded. If a file is
        # selected, it takes precedence over text in that instrument's textarea.
        uploads = [
            ('doc1_file', 'Instrument 1', 'doc1'),
            ('doc2_file', 'Instrument 2', 'doc2'),
        ]
        extracted = {'doc1': doc1_text, 'doc2': doc2_text}
        sources = {'doc1': doc1_source, 'doc2': doc2_source}

        for field_name, label, key in uploads:
            uploaded = request.files.get(field_name)
            if uploaded and uploaded.filename:
                if not allowed_file(uploaded.filename):
                    flash(f"{label}: unsupported file type. Use PDF, DOCX, TXT or a supported image.", "danger")
                    return render_template('compare.html', comparison=None,
                                           doc1_text=doc1_text, doc2_text=doc2_text)
                suffix = os.path.splitext(secure_filename(uploaded.filename))[1].lower()
                temp_path = None
                try:
                    # Unique temporary names prevent concurrent uploads overwriting
                    # one another or colliding with files in the summarizer.
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix,
                                                     dir=Config.UPLOAD_FOLDER) as temp_file:
                        temp_path = temp_file.name
                        uploaded.save(temp_file)
                    text_value, method_used, page_count = parser.parse_file(temp_path)
                    if not text_value or len(text_value.strip()) < 20 or text_value.startswith('[Scanned document detected'):
                        raise ValueError("No readable text was extracted. If this is a scanned PDF/image, ensure Tesseract OCR is installed.")
                    extracted[key] = text_value.strip()
                    sources[key] = f"{uploaded.filename} — {method_used}"
                except Exception as exc:
                    flash(f"Could not read {label}: {exc}", "danger")
                    return render_template('compare.html', comparison=None,
                                           doc1_text=doc1_text, doc2_text=doc2_text)
                finally:
                    if temp_path and os.path.exists(temp_path):
                        try:
                            os.remove(temp_path)
                        except OSError:
                            pass

        doc1_text, doc2_text = extracted['doc1'], extracted['doc2']
        doc1_source, doc2_source = sources['doc1'], sources['doc2']

        if not doc1_text or not doc2_text:
            flash("For each instrument, either paste its text or upload a PDF, DOCX, TXT or supported image.", "warning")
            return render_template('compare.html', comparison=None,
                                   doc1_text=doc1_text, doc2_text=doc2_text)

        if len(doc1_text) < 20 or len(doc2_text) < 20:
            flash("Both instruments must contain at least 20 readable characters.", "warning")
            return render_template('compare.html', comparison=None,
                                   doc1_text=doc1_text, doc2_text=doc2_text)

        # Summarize and compare the extracted full text, regardless of input method.
        sum1 = summarizer_engine.summarize(doc1_text, ratio=0.25)
        sum2 = summarizer_engine.summarize(doc2_text, ratio=0.25)
        clause_diff = compare_contracts(doc1_text, doc2_text)
        comparison_result = {
            'doc1': sum1,
            'doc2': sum2,
            **clause_diff,
            'risk_delta': sum2['risk_analysis']['score'] - sum1['risk_analysis']['score'],
            'doc1_text': doc1_text,
            'doc2_text': doc2_text,
            'doc1_source': doc1_source,
            'doc2_source': doc2_source,
        }

    return render_template('compare.html', comparison=comparison_result,
                           doc1_text=doc1_text, doc2_text=doc2_text)

@app.route('/glossary')
def glossary():
    """Searchable repository of legal jargon and statutory expressions."""
    from summarizer.legal_knowledge import LEGAL_GLOSSARY
    return render_template('glossary.html', glossary=LEGAL_GLOSSARY)

@app.route('/about')
def about():
    """System architecture and research methodology guide."""
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
