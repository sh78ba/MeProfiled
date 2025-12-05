"""
PDF processing utilities
"""
import io
import PyPDF2
from werkzeug.utils import secure_filename
from config import get_config

config = get_config()


def validate_pdf(filename):
    """
    Validate if file is a PDF
    
    Args:
        filename: Name of the file
        
    Returns:
        bool: True if valid PDF filename
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'


def extract_text_from_pdf(pdf_file):
    """
    Extract text from PDF file with enhanced error handling
    
    Args:
        pdf_file: File object or BytesIO containing PDF
        
    Returns:
        str: Extracted text or None if extraction fails
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Check if PDF is encrypted
        if pdf_reader.is_encrypted:
            print("Encrypted PDF detected")
            return None
        
        # Check page count
        page_count = len(pdf_reader.pages)
        if page_count == 0:
            print("PDF has no pages")
            return None
        
        if page_count > config.MAX_PDF_PAGES:
            print(f"PDF has {page_count} pages, limiting to first {config.MAX_PDF_PAGES}")
            page_count = config.MAX_PDF_PAGES
        
        # Extract text from all pages
        text = ""
        for i in range(page_count):
            page_text = pdf_reader.pages[i].extract_text()
            if page_text:
                text += page_text + "\n"
        
        # Validate extracted text length
        if len(text.strip()) < config.MIN_RESUME_TEXT_LENGTH:
            print(f"Extracted text is too short: {len(text.strip())} chars")
            return None
            
        return text.strip()
    except Exception as e:
        logger.error(f"Error reading PDF: {str(e)}", exc_info=True)
        return None


def get_secure_filename(filename):
    """
    Get secure version of filename
    
    Args:
        filename: Original filename
        
    Returns:
        str: Secure filename
    """
    return secure_filename(filename)
