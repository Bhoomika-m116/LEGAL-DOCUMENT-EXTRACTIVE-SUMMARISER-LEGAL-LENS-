import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from config import Config

class LegalReportGenerator:
    def __init__(self):
        os.makedirs(Config.REPORT_FOLDER, exist_ok=True)

    def generate_pdf(self, filename_base, doc_name, summary_data):
        """
        Generates an official formatted PDF legal brief.
        Returns the absolute filepath to the created PDF.
        """
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        out_filename = f"LegalBrief_{filename_base}_{timestamp_str}.pdf"
        out_path = os.path.join(Config.REPORT_FOLDER, out_filename)

        doc = SimpleDocTemplate(
            out_path,
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()
        
        # Custom Professional Styles
        title_style = ParagraphStyle(
            'OfficialTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            textColor=colors.HexColor('#0B192C'),
            alignment=1  # Center
        )
        subtitle_style = ParagraphStyle(
            'OfficialSub',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#555555'),
            alignment=1
        )
        h2_style = ParagraphStyle(
            'SectionH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=colors.HexColor('#1E3E62'),
            spaceBefore=12,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'BodySummary',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#222222')
        )
        bullet_style = ParagraphStyle(
            'BulletStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor('#222222'),
            leftIndent=12,
            firstLineIndent=-10
        )
        callout_style = ParagraphStyle(
            'CalloutStyle',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#444444')
        )

        elements = []

        # 1. Header Banner
        elements.append(Paragraph("<b>LEGAL DOCUMENT EXTRACTIVE SUMMARY BRIEF</b>", title_style))
        elements.append(Paragraph("AI-Powered Legal NLP Analytics & Clause Extraction Engine", subtitle_style))
        elements.append(Spacer(1, 10))
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0B192C'), spaceBefore=2, spaceAfter=12))

        # 2. Key Metadata & Metrics Summary Table
        meta_data = [
            [
                Paragraph("<b>Document Analyzed:</b>", body_style),
                Paragraph(doc_name, body_style),
                Paragraph("<b>Extractive Accuracy:</b>", body_style),
                Paragraph(f"<b><font color='#16a34a'>{summary_data.get('accuracy_score', 0)}%</font></b>", body_style)
            ],
            [
                Paragraph("<b>Original Word Count:</b>", body_style),
                Paragraph(f"{summary_data.get('original_words', 0)} words", body_style),
                Paragraph("<b>Summary Word Count:</b>", body_style),
                Paragraph(f"{summary_data.get('summary_words', 0)} words", body_style)
            ],
            [
                Paragraph("<b>Compression Ratio:</b>", body_style),
                Paragraph(f"{summary_data.get('compression_ratio', 0)}% saved", body_style),
                Paragraph("<b>Risk Classification:</b>", body_style),
                Paragraph(f"<b>{summary_data.get('risk_analysis', {}).get('level', 'Low')}</b>", body_style)
            ],
            [
                Paragraph("<b>Generated On:</b>", body_style),
                Paragraph(datetime.now().strftime("%B %d, %Y - %I:%M %p"), body_style),
                Paragraph("<b>Algorithm Engine:</b>", body_style),
                Paragraph("Hybrid (TextRank + TF-IDF)", body_style)
            ]
        ]
        
        meta_table = Table(meta_data, colWidths=[130, 140, 130, 130])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('PADDING', (0,0), (-1,-1), 5),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(meta_table)
        elements.append(Spacer(1, 14))

        # 3. Executive Extractive Summary Section
        elements.append(Paragraph("1. Executive Extractive Summary", h2_style))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=8))
        
        summary_sentences = summary_data.get('summary_sentences', [])
        if summary_sentences:
            for s in summary_sentences:
                elements.append(Paragraph(f"&bull; {s}", bullet_style))
                elements.append(Spacer(1, 4))
        else:
            elements.append(Paragraph(summary_data.get('summary_text', 'No summary generated.'), body_style))

        elements.append(Spacer(1, 12))

        # 4. Critical Legal Clauses Identified
        clauses = summary_data.get('clauses', {})
        if clauses:
            elements.append(Paragraph("2. Critical Legal Clauses & Covenant Categorization", h2_style))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=8))
            
            for c_name, c_info in list(clauses.items())[:6]:
                elements.append(Paragraph(f"<b>&bull; {c_name}</b>", body_style))
                for sent in c_info.get('sentences', [])[:2]:
                    elements.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;<i>\"{sent[:250]}...\"</i>", callout_style))
                elements.append(Spacer(1, 4))
            elements.append(Spacer(1, 10))

        # 5. Legalese & Complex Terminology Decoded
        legalese = summary_data.get('legalese', [])
        if legalese:
            elements.append(Paragraph("3. Complex Legal Terminology & Plain-English Meanings", h2_style))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=1, spaceAfter=8))
            
            term_rows = [[Paragraph("<b>Legal Term</b>", body_style), Paragraph("<b>Plain-English Interpretation</b>", body_style)]]
            for t in legalese[:6]:
                term_rows.append([
                    Paragraph(f"<b>{t['term']}</b>", body_style),
                    Paragraph(t['plain'], body_style)
                ])
                
            term_table = Table(term_rows, colWidths=[150, 380])
            term_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                ('PADDING', (0,0), (-1,-1), 5),
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ]))
            elements.append(term_table)
            elements.append(Spacer(1, 12))

        # 6. Official Verification Footer
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0B192C'), spaceBefore=10, spaceAfter=6))
        elements.append(Paragraph("<b>CONFIDENTIALITY NOTICE & DISCLAIMER:</b> This extractive summary is automatically compiled using Natural Language Processing (NLP) and graph ranking heuristics (TextRank + TF-IDF). It is an advisory aid and does not constitute formal legal counsel. Verify all clauses against the original executed instrument.", subtitle_style))

        # Build document
        doc.build(elements)
        return out_path
