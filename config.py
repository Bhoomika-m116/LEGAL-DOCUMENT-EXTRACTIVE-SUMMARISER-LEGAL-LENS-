import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'legallens_secure_official_sum_key_2026')
    DATABASE_PATH = os.path.join(BASE_DIR, 'data', 'legallens.db')
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    REPORT_FOLDER = os.path.join(BASE_DIR, 'reports')
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 MB max upload
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'png', 'jpg', 'jpeg', 'tiff', 'bmp'}
    
    # NLP & Extractive Summarization Settings
    DEFAULT_SUMMARY_RATIO = 0.25  # 25% length
    MIN_SUMMARY_SENTENCES = 3
    MAX_SUMMARY_SENTENCES = 25
    TEXTRANK_DAMPING = 0.85
    TEXTRANK_CONVERGENCE = 0.0001
    TEXTRANK_MAX_ITER = 100
    
    # OCR Settings
    TESSERACT_CMD = os.environ.get('TESSERACT_CMD', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
