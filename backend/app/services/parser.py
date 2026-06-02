import PyPDF2
import io
import logging

logger = logging.getLogger("uvicorn.error")

def parse_resume_pdf(file_bytes: bytes) -> str:
    """
    Extracts text from binary PDF bytes using PyPDF2.
    Falls back gracefully if the document structure is corrupted or unreadable.
    """
    text_content = []
    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        
        # Loop through pages and extract plain text
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            extracted = page.extract_text()
            if extracted:
                text_content.append(extracted)
                
        full_text = "\n".join(text_content).strip()
        
        if not full_text:
            logger.warning("PDF parsing resulted in empty text. Document may contain scanned images only.")
            return "[Empty or scanned PDF document]"
            
        return full_text
    except Exception as e:
        logger.error(f"Error parsing PDF resume document: {str(e)}")
        return f"[Failed to extract text from PDF: {str(e)}]"

def parse_resume_bytes(file_bytes: bytes, filename: str) -> str:
    """
    Parses resume files based on their extensions.
    Currently supports PDF and plain text.
    """
    fn = filename.lower()
    if fn.endswith(".pdf"):
        return parse_resume_pdf(file_bytes)
    elif fn.endswith((".txt", ".md", ".json")):
        try:
            return file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return file_bytes.decode("latin-1")
            except Exception as e:
                return f"[Failed to decode plain text document: {str(e)}]"
    else:
        # Fallback raw conversion attempting simple decode or reporting type mismatch
        try:
            return file_bytes.decode("utf-8", errors="ignore")
        except Exception:
            return "[Unsupported non-text file format]"
