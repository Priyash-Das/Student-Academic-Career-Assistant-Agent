from study_buddy.llm.client import call_llm
from study_buddy.llm.prompts import SUMMARY_PROMPT
from study_buddy.config.models import STUDY_SUMMARY_MODEL
from study_buddy.utils.errors import PipelineError
def run_summary_pipeline(study_context: str) -> str:
    if not study_context or not study_context.strip():
        raise PipelineError("Study context is empty. Cannot summarize.")
    prompt = SUMMARY_PROMPT.format(
        study_context=study_context
    )
    try:
        output = call_llm(
            model=STUDY_SUMMARY_MODEL,
            prompt=prompt
        )
    except Exception as e:
        raise PipelineError(
            "Failed to generate summary."
        ) from e
    if not output or not output.strip():
        raise PipelineError(
            "Summary model returned empty output."
        )
    return output.strip()