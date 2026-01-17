from typing import List
from PyPDF2 import PdfReader
from study_buddy.utils.errors import InputValidationError
from study_buddy.config.settings import MAX_PDF_PAGES
def load_pdf_text(pdf_path: str) -> str:
    try:
        reader = PdfReader(pdf_path)
    except Exception:
        raise InputValidationError("Failed to open the PDF file.")
    if len(reader.pages) == 0:
        raise InputValidationError("PDF contains no readable pages.")
    if len(reader.pages) > MAX_PDF_PAGES:
        raise InputValidationError(
            f"PDF exceeds maximum allowed pages ({MAX_PDF_PAGES})."
        )
    pages_text: List[str] = []
    for i, page in enumerate(reader.pages):
        try:
            text = page.extract_text()
        except Exception:
            text = ""
        if text:
            pages_text.append(text.strip())
    if not pages_text:
        raise InputValidationError(
            "No extractable text found in the PDF."
        )
    return "\n\n".join(pages_text)