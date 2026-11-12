import os
import io
import fitz  # PyMuPDF
import pdfplumber
from PIL import Image
import pytesseract
import docx
from config import Config

class DocumentParser:
    def __init__(self):
        # Configure Tesseract path if available on system
        self.tesseract_available = self._setup_tesseract()

    def _setup_tesseract(self):
        """Attempts to locate tesseract executable on Windows."""
        possible_paths = [
            Config.TESSERACT_CMD,
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
            r'C:\Users\pc\AppData\Local\Tesseract-OCR\tesseract.exe',
            r'C:\tools\tesseract\tesseract.exe'
        ]
        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                return True
        return False

    def parse_file(self, filepath, force_ocr=False):
        """
        Parses text from various document formats (.pdf, .docx, .txt, .png, .jpg, etc.).
        Returns: (extracted_text, method_used, page_count)
        """
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.txt':
            return self._parse_txt(filepath)
        elif ext == '.docx':
            return self._parse_docx(filepath)
        elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            return self._parse_image_ocr(filepath)
        elif ext == '.pdf':
            return self._parse_pdf(filepath, force_ocr=force_ocr)
        else:
            raise ValueError(f"Unsupported file format: {ext}")

    def _parse_txt(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                text = f.read()
            return text, "Direct Text Extraction", 1
        except Exception as e:
            with open(filepath, 'r', encoding='latin-1', errors='replace') as f:
                text = f.read()
            return text, "Direct Text Extraction (Latin-1)", 1

    def _parse_docx(self, filepath):
        doc = docx.Document(filepath)
        full_text = []
        for para in doc.paragraphs:
            if para.text.strip():
                full_text.append(para.text.strip())
        
        for table in doc.tables:
            for row in table.rows:
                row_text = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                if row_text:
                    full_text.append(" | ".join(row_text))
                    
        return "\n\n".join(full_text), "DOCX Structure Parser", len(doc.paragraphs)

    def _parse_pdf(self, filepath, force_ocr=False):
        """Extracts text from PDF, falling back to OCR if the PDF is scanned / empty."""
        text = ""
        total_pages = 0
        method = "Digital PDF Stream Extraction"

        # Step 1: Attempt digital text extraction with PyMuPDF (fitz)
        try:
            doc = fitz.open(filepath)
            total_pages = len(doc)
            page_texts = []
            
            for page_num in range(total_pages):
                page = doc[page_num]
                p_text = page.get_text()
                if p_text.strip():
                    page_texts.append(p_text.strip())
            
            doc.close()
            text = "\n\n".join(page_texts)
        except Exception:
            # Fallback to pdfplumber
            try:
                with pdfplumber.open(filepath) as pdf:
                    total_pages = len(pdf.pages)
                    extracted = [p.extract_text() for p in pdf.pages if p.extract_text()]
                    text = "\n\n".join(extracted)
            except Exception:
                text = ""

        # Step 2: If text is negligible (< 100 characters) or force_ocr is enabled, run OCR
        if (len(text.strip()) < 100 or force_ocr) and self.tesseract_available:
            ocr_text, ocr_pages = self._ocr_pdf(filepath)
            if len(ocr_text.strip()) > len(text.strip()):
                text = ocr_text
                method = f"Tesseract Optical Character Recognition (OCR) [{ocr_pages} pages]"

        elif len(text.strip()) < 100 and not self.tesseract_available:
            # Informative message if scanned PDF and tesseract binary is not on host
            if not text.strip():
                text = "[Scanned document detected. Digital text stream empty. Install Tesseract-OCR for scanned image conversion.]"
                method = "Scanned PDF (No embedded text)"

        return text, method, total_pages

    def _ocr_pdf(self, filepath):
        """Extracts images from PDF pages and runs Tesseract OCR."""
        ocr_text = []
        doc = fitz.open(filepath)
        page_count = len(doc)
        
        for i in range(page_count):
            page = doc[i]
            pix = page.get_pixmap(dpi=200)
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            try:
                txt = pytesseract.image_to_string(img)
                if txt.strip():
                    ocr_text.append(f"--- PAGE {i+1} ---\n" + txt.strip())
            except Exception:
                pass
        doc.close()
        return "\n\n".join(ocr_text), page_count

    def _parse_image_ocr(self, filepath):
        """Runs OCR on image files."""
        if not self.tesseract_available:
            return (
                "[OCR Engine Notice: Tesseract executable not detected at standard Windows path. "
                "Please configure Tesseract-OCR to extract text directly from image scans.]",
                "OCR Unavailable",
                1
            )
        try:
            img = Image.open(filepath)
            text = pytesseract.image_to_string(img)
            return text, "Image Tesseract OCR", 1
        except Exception as e:
            return f"Error during OCR extraction: {str(e)}", "OCR Error", 1
