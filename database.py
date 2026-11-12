import sqlite3
import os
import json
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

def get_db_connection():
    os.makedirs(os.path.dirname(Config.DATABASE_PATH), exist_ok=True)
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT,
        organization TEXT,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Document Summaries History table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS summaries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        filename TEXT NOT NULL,
        doc_type TEXT DEFAULT 'Legal Document',
        original_words INTEGER DEFAULT 0,
        summary_words INTEGER DEFAULT 0,
        accuracy_score REAL DEFAULT 0.0,
        compression_ratio REAL DEFAULT 0.0,
        risk_level TEXT DEFAULT 'Low',
        risk_score INTEGER DEFAULT 0,
        clauses_json TEXT,
        legalese_json TEXT,
        summary_text TEXT NOT NULL,
        full_text_preview TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
    )
    ''')
    
    # Create default demo user if not exists
    cursor.execute("SELECT id FROM users WHERE username = 'advocate_demo'")
    if not cursor.fetchone():
        hashed = generate_password_hash("LegalPass2026!")
        cursor.execute('''
        INSERT INTO users (username, email, password_hash, full_name, organization, role)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', ('advocate_demo', 'demo@legallens.gov', hashed, 'Senior Counsel Advocate', 'High Court Bar Association', 'user'))
    
    conn.commit()
    conn.close()

def create_user(username, email, password, full_name='', organization=''):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        pw_hash = generate_password_hash(password)
        cursor.execute('''
        INSERT INTO users (username, email, password_hash, full_name, organization)
        VALUES (?, ?, ?, ?, ?)
        ''', (username.strip(), email.strip().lower(), pw_hash, full_name.strip(), organization.strip()))
        conn.commit()
        user_id = cursor.lastrowid
        return True, user_id
    except sqlite3.IntegrityError as e:
        return False, "Username or email already exists."
    except Exception as e:
        return False, str(e)
    finally:
        conn.close()

def authenticate_user(username_or_email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM users WHERE username = ? OR email = ?
    ''', (username_or_email.strip(), username_or_email.strip().lower()))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def save_summary_record(user_id, filename, doc_type, orig_words, sum_words, 
                        accuracy, compression, risk_level, risk_score, 
                        clauses, legalese, summary_text, preview_text=''):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO summaries (
        user_id, filename, doc_type, original_words, summary_words,
        accuracy_score, compression_ratio, risk_level, risk_score,
        clauses_json, legalese_json, summary_text, full_text_preview
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, filename, doc_type, orig_words, sum_words,
        round(accuracy, 2), round(compression, 2), risk_level, int(risk_score),
        json.dumps(clauses), json.dumps(legalese), summary_text, preview_text[:800]
    ))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id

def get_user_summaries(user_id, limit=50):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute('''
        SELECT * FROM summaries WHERE user_id = ? ORDER BY created_at DESC LIMIT ?
        ''', (user_id, limit))
    else:
        cursor.execute('''
        SELECT * FROM summaries WHERE user_id IS NULL ORDER BY created_at DESC LIMIT ?
        ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        try:
            d['clauses'] = json.loads(d['clauses_json']) if d['clauses_json'] else []
        except:
            d['clauses'] = []
        try:
            d['legalese'] = json.loads(d['legalese_json']) if d['legalese_json'] else []
        except:
            d['legalese'] = []
        results.append(d)
    return results

def get_summary_by_id(summary_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM summaries WHERE id = ?', (summary_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    try:
        d['clauses'] = json.loads(d['clauses_json']) if d['clauses_json'] else []
    except:
        d['clauses'] = []
    try:
        d['legalese'] = json.loads(d['legalese_json']) if d['legalese_json'] else []
    except:
        d['legalese'] = []
    return d

def delete_summary(summary_id, user_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if user_id:
        cursor.execute('DELETE FROM summaries WHERE id = ? AND user_id = ?', (summary_id, user_id))
    else:
        cursor.execute('DELETE FROM summaries WHERE id = ?', (summary_id,))
    conn.commit()
    conn.close()
    return True
