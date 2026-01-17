from study_buddy.llm.client import call_llm
from study_buddy.llm.prompts import QUIZ_PROMPT
from study_buddy.config.models import STUDY_QUIZ_MODEL
from study_buddy.utils.errors import PipelineError
def run_quiz_pipeline(study_context: str) -> str:
    if not study_context or not study_context.strip():
        raise PipelineError("Study context is empty. Cannot generate quiz.")
    if len(study_context.strip()) < 200:
        raise PipelineError(
            "Insufficient factual study material to generate a quiz."
        )
    prompt = QUIZ_PROMPT.format(
        study_context=study_context
    )
    try:
        output = call_llm(
            model=STUDY_QUIZ_MODEL,
            prompt=prompt
        )
    except Exception:
        return _fallback_quiz(study_context)
    if not output or not output.strip():
        return _fallback_quiz(study_context)
    return output.strip()
def _fallback_quiz(study_context: str) -> str:
    return (
        "Quiz (Fallback Mode):\n\n"
        "Sorry - an internal error has occurred. The model is currently not functioning."
    )
