import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, 
    Preformatted, Table, TableStyle, HRFlowable
)
import pypdf

BASE_DIR = r"c:\Users\pc\OneDrive\Desktop\final"
DESKTOP_DIR = r"c:\Users\pc\OneDrive\Desktop"
ORIGINAL_P1 = os.path.join(DESKTOP_DIR, "p1.pdf")

OUTPUT_CODEBOOK_PDF = os.path.join(BASE_DIR, "Legal_Extractive_Summarizer_Complete_Project_Code_Book.pdf")
OUTPUT_DESKTOP_CODEBOOK_PDF = os.path.join(DESKTOP_DIR, "LegalLens_Project_Complete_Source_Code.pdf")
OUTPUT_MERGED_P1_PDF = os.path.join(DESKTOP_DIR, "p1_Complete_Project_Report_with_Source_Code.pdf")
OUTPUT_FINAL_MERGED_PDF = os.path.join(BASE_DIR, "p1_Complete_Project_Report_with_Source_Code.pdf")

# Files to include in the complete codebook
SOURCE_FILES = [
    ("Application Entrypoint", "app.py", "Python / Flask"),
    ("Configuration Settings", "config.py", "Python"),
    ("Database & User Management", "database.py", "Python / SQLite"),
    ("NLP Preprocessor", os.path.join("summarizer", "nlp_preprocessor.py"), "Python / NLTK"),
    ("OCR & Document Parser", os.path.join("summarizer", "ocr_parser.py"), "Python / Tesseract / PyMuPDF"),
    ("Legal Knowledge & Clause Engine", os.path.join("summarizer", "legal_knowledge.py"), "Python"),
    ("Scientific Metrics Calculator", os.path.join("summarizer", "metrics.py"), "Python / Scikit-Learn"),
    ("Extractive Summarizer Engine", os.path.join("summarizer", "extractive_engine.py"), "Python / TextRank / TF-IDF"),
    ("PDF Legal Brief Generator", os.path.join("summarizer", "report_generator.py"), "Python / ReportLab"),
    ("Master Base Template", os.path.join("templates", "base.html"), "HTML5 / Jinja2 / Bootstrap 5"),
    ("Official Home Portal", os.path.join("templates", "index.html"), "HTML5 / Jinja2 / CSS Animations"),
    ("Practitioner Login Template", os.path.join("templates", "login.html"), "HTML5 / Jinja2"),
    ("Practitioner Registration", os.path.join("templates", "register.html"), "HTML5 / Jinja2"),
    ("Interactive Workroom Dashboard", os.path.join("templates", "dashboard.html"), "HTML5 / Jinja2"),
    ("Extractive Summary Result View", os.path.join("templates", "result.html"), "HTML5 / Jinja2"),
    ("Audit History Ledger Template", os.path.join("templates", "history.html"), "HTML5 / Jinja2"),
    ("Contract Redline Comparison", os.path.join("templates", "compare.html"), "HTML5 / Jinja2"),
    ("Statutory Glossary Template", os.path.join("templates", "glossary.html"), "HTML5 / Jinja2"),
    ("System Architecture & About", os.path.join("templates", "about.html"), "HTML5 / Jinja2"),
    ("Official Styling Stylesheet", os.path.join("static", "css", "style.css"), "CSS3"),
    ("Moving Images & Keyframes", os.path.join("static", "css", "animations.css"), "CSS3"),
    ("Client-side Interactive Engine", os.path.join("static", "js", "main.js"), "JavaScript (ES6+)"),
    ("Project Dependencies", "requirements.txt", "Configuration"),
    ("Windows 1-Click Launcher", "run.bat", "Batch Script"),
]

def build_codebook_pdf(output_path):
    print(f"Building complete codebook PDF at: {output_path} ...")
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0B192C'),
        alignment=1,
        spaceAfter=15
    )

    sub_style = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=10
    )

    h1_style = ParagraphStyle(
        'SecHeading1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#0B192C'),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    code_title_style = ParagraphStyle(
        'CodeTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E3E62'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    code_body_style = ParagraphStyle(
        'CodeBody',
        fontName='Courier',
        fontSize=6.5,
        leading=8.2,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=2,
        spaceAfter=6
    )

    elements = []

    # 1. Cover Page
    elements.append(Spacer(1, 40))
    elements.append(Paragraph("<b>LEGAL DOCUMENT EXTRACTIVE SUMMARISER</b>", title_style))
    elements.append(Paragraph("<b>PROJECT PHASE-II (BCS685) &bull; COMPLETE SOURCE CODE COMPENDIUM</b>", ParagraphStyle('SubGold', parent=sub_style, fontName='Helvetica-Bold', textColor=colors.HexColor('#B8972E'), fontSize=13)))
    elements.append(Spacer(1, 15))
    elements.append(HRFlowable(width="100%", thickness=2.5, color=colors.HexColor('#0B192C'), spaceBefore=5, spaceAfter=20))
    elements.append(Paragraph("<b>Department of Computer Science and Engineering</b><br/>Ghousia Institute of Technology for Women", sub_style))
    elements.append(Spacer(1, 25))

    # Architecture Overview Table on Cover
    table_data = [
        [Paragraph("<b>Domain</b>", sub_style), Paragraph("Legal Document Extractive Intelligence & Compliance", sub_style)],
        [Paragraph("<b>Core Technologies</b>", sub_style), Paragraph("NLP, Tesseract OCR, TextRank PageRank, TF-IDF, Flask, Bootstrap 5, Jinja2", sub_style)],
        [Paragraph("<b>Key Features</b>", sub_style), Paragraph("Dual Extractive Ranking, 12-Clause Extractor, 40+ Latin Legalese Decoder, Semantic Accuracy %, Risk Audit Meter, Redline Comparison, Audio Narrator (TTS), Official PDF Export, Guest Mode", sub_style)],
        [Paragraph("<b>Total Source Modules</b>", sub_style), Paragraph(f"{len(SOURCE_FILES)} Full Code Files Included", sub_style)],
    ]
    info_table = Table(table_data, colWidths=[150, 390])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 30))
    elements.append(Paragraph("<i>This compendium contains the full verified source code listings for all modules of the new LegalLens system.</i>", sub_style))
    elements.append(PageBreak())

    # 2. Table of Contents / File Index
    elements.append(Paragraph("<b>PROJECT SOURCE CODE INVENTORY</b>", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0B192C'), spaceBefore=2, spaceAfter=12))

    idx_data = [[
        Paragraph("<b>#</b>", sub_style),
        Paragraph("<b>Module Name</b>", sub_style),
        Paragraph("<b>Relative Filepath</b>", sub_style),
        Paragraph("<b>Technology Stack</b>", sub_style)
    ]]

    for i, (title, rel_path, tech) in enumerate(SOURCE_FILES, 1):
        idx_data.append([
            Paragraph(str(i), sub_style),
            Paragraph(f"<b>{title}</b>", sub_style),
            Paragraph(f"<code>{rel_path}</code>", sub_style),
            Paragraph(tech, sub_style)
        ])

    idx_table = Table(idx_data, colWidths=[25, 175, 210, 130])
    idx_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0B192C')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(idx_table)
    elements.append(PageBreak())

    # 3. Source Code Listings
    for i, (title, rel_path, tech) in enumerate(SOURCE_FILES, 1):
        full_path = os.path.join(BASE_DIR, rel_path)
        if not os.path.exists(full_path):
            continue

        try:
            with open(full_path, 'r', encoding='utf-8', errors='replace') as f:
                code_content = f.read()
        except Exception:
            code_content = "# File content unavailable."

        # Header for this file
        banner_text = f"<b>FILE #{i}: {title}</b> &mdash; <code>{rel_path}</code> ({tech})"
        elements.append(Paragraph(banner_text, code_title_style))
        elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#1E3E62'), spaceBefore=2, spaceAfter=6))

        # Add line numbers
        lines = code_content.split('\n')
        numbered_lines = []
        for line_num, l in enumerate(lines, 1):
            # Clean tabs
            l_clean = l.replace('\t', '    ')
            numbered_lines.append(f"{line_num:4d} | {l_clean}")

        chunk_text = "\n".join(numbered_lines)
        
        # Split into manageable blocks if huge
        max_chars_per_block = 8000
        for block_start in range(0, len(chunk_text), max_chars_per_block):
            block = chunk_text[block_start:block_start + max_chars_per_block]
            pre = Preformatted(block, code_body_style)
            elements.append(pre)

        elements.append(Spacer(1, 14))

    # Build the PDF
    doc.build(elements)
    print("PDF build successful.")

def merge_with_p1():
    """Appends the newly generated codebook directly to the user's p1.pdf."""
    if not os.path.exists(ORIGINAL_P1):
        print(f"Original p1.pdf not found at {ORIGINAL_P1}.")
        return

    print("Merging source code compendium into original p1.pdf...")
    writer = pypdf.PdfWriter()
    writer.append(ORIGINAL_P1)
    writer.append(OUTPUT_CODEBOOK_PDF)

    with open(OUTPUT_MERGED_P1_PDF, "wb") as f_out:
        writer.write(f_out)
    with open(OUTPUT_FINAL_MERGED_PDF, "wb") as f_out2:
        writer.write(f_out2)
    writer.close()
    print(f"Successfully created merged comprehensive report: {OUTPUT_MERGED_P1_PDF}")

if __name__ == '__main__':
    # 1. Build standalone codebook in final/
    build_codebook_pdf(OUTPUT_CODEBOOK_PDF)

    # 2. Copy codebook to Desktop as well for convenience
    import shutil
    shutil.copyfile(OUTPUT_CODEBOOK_PDF, OUTPUT_DESKTOP_CODEBOOK_PDF)
    print(f"Copied standalone codebook to Desktop: {OUTPUT_DESKTOP_CODEBOOK_PDF}")

    # 3. Merge with p1.pdf
    merge_with_p1()
    print("All PDF generations and merges complete!")
