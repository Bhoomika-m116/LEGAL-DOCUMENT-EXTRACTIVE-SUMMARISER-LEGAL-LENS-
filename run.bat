@echo off
title LegalLens - Extractive Legal Document Summarizer Portal
echo =========================================================================
echo   LEGALLENS - OFFICIAL LEGAL DOCUMENT EXTRACTIVE SUMMARIZER
echo   NLP | OCR | TextRank | TF-IDF | Flask | Bootstrap 5
echo =========================================================================
echo.
echo [1/2] Checking Python runtime...
python --version
if errorlevel 1 (
    echo [ERROR] Python not detected. Please install Python 3.10+ and add to PATH.
    pause
    exit /b 1
)

echo.
echo [2/2] Launching LegalLens Portal on http://127.0.0.1:5000 ...
echo [INFO] Press Ctrl+C in this terminal window to stop the server.
echo.
python app.py
pause
