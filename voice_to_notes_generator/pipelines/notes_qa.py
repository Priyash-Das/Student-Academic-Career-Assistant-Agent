from voice_to_notes_generator.config.models import NOTES_QA_MODEL, GROQ_API_KEY
from voice_to_notes_generator.utils.prompt_templates import notes_qa_prompt
from voice_to_notes_generator.utils.safety import enforce_notes_qa_answer
from voice_to_notes_generator.config.settings import QA_MAX_TOKENS
from voice_to_notes_generator.state.lecture_state import lecture_state
class NotesQAError(Exception):
    pass
def answer_from_notes(question: str) -> str:
    if not question or not question.strip():
        raise NotesQAError("Question cannot be empty.")
    if not lecture_state.has_notes():
        raise NotesQAError("Lecture notes are not available yet.")
    notes = lecture_state.get_notes_for_qa()
    prompt = notes_qa_prompt(notes=notes, question=question)
    try:
        answer = _query_notes_model(prompt)
        return enforce_notes_qa_answer(answer)
    except Exception as e:
        raise NotesQAError(f"Notes Q&A failed: {str(e)}")
def _query_notes_model(prompt: str) -> str:
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model=NOTES_QA_MODEL,
            messages=[
                {"role": "system", "content": "You are a strict academic assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=QA_MAX_TOKENS,
        )
        return completion.choices[0].message.content or ""
    except Exception as e:
        raise NotesQAError(f"Model invocation error: {e}")