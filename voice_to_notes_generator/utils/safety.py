from voice_to_notes_generator.config.settings import STRICT_QA_FALLBACK_MESSAGE
def validate_notes_output(text: str) -> str:
    if not text or len(text.strip()) < 100:
        raise ValueError("Generated notes are empty or too short.")
    forbidden_phrases = [
        "for example, imagine",
        "it is widely known",
        "in general",
        "typically",
    ]
    for phrase in forbidden_phrases:
        if phrase in text.lower():
            raise ValueError("Potential hallucination detected in notes.")
    return text.strip()
def enforce_notes_qa_answer(answer: str) -> str:
    if not answer:
        return STRICT_QA_FALLBACK_MESSAGE
    normalized = answer.strip().lower()
    fallback = STRICT_QA_FALLBACK_MESSAGE.lower()
    if fallback in normalized:
        return STRICT_QA_FALLBACK_MESSAGE
    return answer.strip()