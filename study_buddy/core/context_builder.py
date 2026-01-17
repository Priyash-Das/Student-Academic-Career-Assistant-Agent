from typing import List
from study_buddy.core.chunker import chunk_text
from study_buddy.core.pdf_loader import load_pdf_text
from study_buddy.llm.client import call_llm
from study_buddy.llm.prompts import (
    READER_PDF_ONLY_PROMPT,
    READER_PROMPT_PDF_PROMPT,
)
from study_buddy.config.models import STUDY_READER_MODEL
from study_buddy.utils.errors import ContextBuildError
def build_study_context(
    input_mode: str,
    prompt: str = "",
    pdf_path: str = ""
) -> str:
    if input_mode == "PROMPT_ONLY":
        return (
            "STUDY MATERIAL PROVIDED BY USER:\n"
            + prompt.strip()
        )
    if input_mode not in ("PDF_ONLY", "PROMPT_PDF"):
        raise ContextBuildError("Invalid input mode.")
    raw_pdf_text = load_pdf_text(pdf_path)
    chunks = chunk_text(raw_pdf_text)
    if not chunks:
        raise ContextBuildError("Failed to extract content from PDF.")
    prepared_context_parts: List[str] = []
    success_count = 0
    for chunk in chunks:
        if input_mode == "PDF_ONLY":
            reader_prompt = READER_PDF_ONLY_PROMPT.format(
                pdf_chunk=chunk
            )
        else:  
            reader_prompt = READER_PROMPT_PDF_PROMPT.format(
                pdf_chunk=chunk,
                user_prompt=prompt
            )
        try:
            cleaned = call_llm(
                model=STUDY_READER_MODEL,
                prompt=reader_prompt
            )
            if cleaned and cleaned.strip():
                prepared_context_parts.append(cleaned.strip())
                success_count += 1
        except Exception:
            continue  
    if success_count == 0:
        return (
            "RAW STUDY MATERIAL FROM PDF:\n"
            + raw_pdf_text[:8000]
        )
    return "\n\n".join(prepared_context_parts)