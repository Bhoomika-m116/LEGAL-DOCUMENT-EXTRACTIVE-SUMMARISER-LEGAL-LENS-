# LegalLens: Official Legal Document Extractive Summarizer

An official, enterprise-grade statutory and legal document extractive summarization platform engineered with **Natural Language Processing (NLP)**, **Optical Character Recognition (OCR)**, **TextRank Graph PageRank**, **TF-IDF Saliency Centroids**, and **Calibrated Extractive Accuracy Metrics**.

---

## 🏛️ System Architecture Overview

```
                      +------------------------------------------+
                      |       Input Legal Instrument             |
                      |  (PDF / Scanned Image / DOCX / Text)     |
                      +--------------------+---------------------+
                                           |
                                           v
                      +------------------------------------------+
                      |         Document Ingestion & OCR         |
                      |  - Digital PyMuPDF text stream           |
                      |  - Tesseract OCR (200 DPI binarization)  |
                      +--------------------+---------------------+
                                           |
                                           v
                      +------------------------------------------+
                      |        Legal NLP Preprocessor            |
                      |  - Legal citation boundary shield        |
                      |  - Statutory stopword pruning            |
                      |  - WordNet lemmatization                 |
                      +--------------------+---------------------+
                                           |
                    +----------------------+----------------------+
                    |                                             |
                    v                                             v
        +-----------------------+                     +-----------------------+
        |   TextRank Engine     |                     |    TF-IDF Centroid    |
        | - Cosine sim graph    |                     | - Document mean vec   |
        | - PageRank power iter |                     | - Centroid distance   |
        | - Damping (d = 0.85)  |                     | - Operative cues      |
        +-----------+-----------+                     +-----------+-----------+
                    |                                             |
                    +----------------------+----------------------+
                                           |
                                           v
                      +------------------------------------------+
                      |     Hybrid Extractive Ensemble & MMR     |
                      |  Score = 0.45*TR + 0.35*TFIDF + 0.20*Cue |
                      |  Maximal Marginal Relevance (Diversity)   |
                      +--------------------+---------------------+
                                           |
                                           v
                      +------------------------------------------+
                      |     Clause Extractor & Legalese Decoder  |
                      |  - 12 standard contract covenants        |
                      |  - 40+ Latin & complex terms translated  |
                      |  - Contract Risk & Safety index (0-100)  |
                      +--------------------+---------------------+
                                           |
                                           v
                      +------------------------------------------+
                      |       Extractive Accuracy Evaluation     |
                      |  - Cosine Semantic Coverage Metric       |
                      |  - Compression Ratio (% & minutes saved) |
                      |  - Flesch-Kincaid Readability Grading    |
                      +--------------------+---------------------+
                                           |
                                           v
                      +------------------------------------------+
                      |  Interactive Web Portal & PDF Generation |
                      |  - Animated moving legal figures & hero  |
                      |  - Web Speech TTS Audio voice playback   |
                      |  - Official downloadable PDF brief       |
                      |  - Contract Redline Comparison Mode      |
                      |  - Login, Register & Instant Guest Mode  |
                      +------------------------------------------+
```

---

## 🚀 Key Features

1. **Dual-Engine Extractive Summarization**:
   - PageRank graph ranking over sentence similarity matrices.
   - TF-IDF centroid distance ranking.
   - Positional and statutory keyword heuristics.
2. **Optical Character Recognition (OCR)**:
   - Scans camera photos, affidavits, and non-selectable PDFs using Tesseract OCR and PyMuPDF.
3. **Legalese Decoder & Plain-English Glossary**:
   - Detects Latin maxims (*indemnification, mutatis mutandis, ultra vires, liquidated damages, subrogation, quantum meruit*) and maps them into clear layman definitions with context snippets.
4. **Contract Risk Audit & Red-Flag Meter**:
   - Audits uncapped indemnities, unilateral termination rights, liquidated penalties, and forum shopping.
5. **Contract Redline & Version Compare Mode**:
   - Compare two contract drafts side-by-side to identify deleted, added, or modified covenants.
6. **Web Speech API Audio Narrator (TTS)**:
   - Listen to executive legal summaries with play, pause, and stop controls.
7. **Extractive Accuracy & Scientific Metrics**:
   - Calibrated Semantic Vector Cosine Similarity score (0-100%).
   - Word count compression ratio and estimated time saved.
   - Flesch-Kincaid Readability Grade Level before and after extraction.
8. **Multi-Tier Authentication & Instant Guest Mode**:
   - Secure SQLite database authentication with hashed passwords (`werkzeug.security`).
   - One-click Guest Practitioner mode for immediate evaluations without registration.
9. **Official PDF Legal Brief Export**:
   - Generates publication-ready PDF briefs with institutional seals and metrics via ReportLab.

---

## 🛠️ Quick Start

### 1. Launch with One Click
Double click `run.bat` in the project root folder.

### 2. Manual Launch
```bash
python -m pip install -r requirements.txt
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 3. Demo Credentials
- **Username:** `advocate_demo`
- **Password:** `LegalPass2026!`
- *Or simply click **"Guest Mode"** on the top navigation bar.*
