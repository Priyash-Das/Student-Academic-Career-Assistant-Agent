from typing import Optional, Literal
from study_buddy.utils.errors import InputValidationError
from study_buddy.config.settings import MAX_PDF_SIZE_MB
InputMode = Literal["PROMPT_ONLY", "PROMPT_NOTES", "PDF_ONLY", "PROMPT_PDF"]
def detect_input_mode(
    prompt: Optional[str],
    pdf_path: Optional[str]
) -> InputMode:
    prompt = (prompt or "").strip()
    if prompt and pdf_path:
        return "PROMPT_PDF"
    if prompt and not pdf_path:
        if is_factual_notes(prompt):
            return "PROMPT_NOTES"
        return "PROMPT_ONLY"
    if pdf_path and not prompt:
        return "PDF_ONLY"
    raise InputValidationError(
        "Please provide a prompt, a PDF, or both."
    )
def validate_prompt(prompt: Optional[str]) -> str:
    if not prompt:
        return ""
    prompt = prompt.strip()
    if not prompt:
        raise InputValidationError("Prompt cannot be empty.")
    if len(prompt) < 3:
        raise InputValidationError(
            "Prompt is too short to be meaningful."
        )
    return prompt
def validate_pdf(pdf_path: Optional[str]) -> str:
    if not pdf_path:
        return ""
    if not pdf_path.lower().endswith(".pdf"):
        raise InputValidationError("Only PDF files are supported.")
    try:
        import os
        size_mb = os.path.getsize(pdf_path) / (1024 * 1024)
    except OSError:
        raise InputValidationError("Unable to read the PDF file.")
    if size_mb > MAX_PDF_SIZE_MB:
        raise InputValidationError(
            f"PDF exceeds size limit of {MAX_PDF_SIZE_MB} MB."
        )
    return pdf_path
def validate_inputs(
    prompt: Optional[str],
    pdf_path: Optional[str]
) -> InputMode:
    clean_prompt = validate_prompt(prompt)
    clean_pdf = validate_pdf(pdf_path)
    mode = detect_input_mode(clean_prompt, clean_pdf)
    if mode == "PROMPT_ONLY":
        if is_question_like(clean_prompt):
            raise InputValidationError(
                "Prompt-only mode requires study material, not a question. "
                "Please upload a PDF or provide factual notes."
            )
    return mode
def is_question_like(text: str) -> bool:
    text = text.lower().strip()
    question_mark = "?" in text
    starts_like_question = text.startswith((
        "what", "why", "how", "explain", "describe",
        "tell me", "can you", "could you", "to dive",
        "perhaps explore"
    ))
    return question_mark or starts_like_question
def is_factual_notes(text: str) -> bool:
    text = text.strip()
    if len(text) < 200:
        return False
    lower = text.lower()
    question_markers = (
        "what ", "why ", "how ", "explain ",
        "describe ", "?", "can you", "could you"
    )
    return not any(marker in lower for marker in question_markers)