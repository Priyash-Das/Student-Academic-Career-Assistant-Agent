from voice_to_notes_generator.config.models import NOTES_QA_MODEL, GROQ_API_KEY
from voice_to_notes_generator.utils.prompt_templates import explain_answer_prompt
from voice_to_notes_generator.state.lecture_state import lecture_state
class ExplainAnswerError(Exception):
    pass
def explain_answer(answer: str) -> str:
    if not lecture_state.has_notes():
        raise ExplainAnswerError("Lecture notes not available.")
    notes = lecture_state.get_notes_for_qa()
    prompt = explain_answer_prompt(notes, answer)
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model=NOTES_QA_MODEL, 
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful academic tutor who explains concepts clearly."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=700
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        raise ExplainAnswerError(str(e))