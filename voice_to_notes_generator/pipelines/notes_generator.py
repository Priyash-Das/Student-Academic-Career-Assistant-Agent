from typing import List
import google.generativeai as genai
from voice_to_notes_generator.config.models import LECTURE_NOTES_MODEL, GOOGLE_API_KEY
from voice_to_notes_generator.utils.prompt_templates import lecture_notes_prompt
from voice_to_notes_generator.utils.safety import validate_notes_output
from voice_to_notes_generator.utils.chunking import chunk_text
class NotesGenerationError(Exception):
    pass
def generate_structured_notes(transcript: str) -> str:
    if not transcript or not transcript.strip():
        raise NotesGenerationError("Transcript is empty. Cannot generate notes.")
    if len(transcript) < 500000:
        return _generate_full_notes(transcript)
    else:
        return _generate_chunked_notes(transcript)
def _generate_full_notes(transcript: str) -> str:
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel(LECTURE_NOTES_MODEL)
        prompt = lecture_notes_prompt(transcript)
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "top_p": 0.95,
                "max_output_tokens": 8192, 
            },
        )
        if not response.text:
            raise NotesGenerationError("LLM returned empty response.")
        return validate_notes_output(response.text)
    except Exception as e:
        raise NotesGenerationError(f"Full notes generation failed: {str(e)}")
def _generate_chunked_notes(transcript: str) -> str:
    chunks = chunk_text(transcript, max_size=50000) 
    partial_notes: List[str] = []
    for idx, chunk in enumerate(chunks):
        try:
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel(LECTURE_NOTES_MODEL)
            chunk_prompt = f"""
            You are processing PART {idx+1} of a long lecture.
            Extract key information, definitions, and concepts from this section.
            Do not write a main Title or Overview yet. Just bullet points and explanations.
            
            TRANSCRIPT PART:
            {chunk}
            """
            response = model.generate_content(
                chunk_prompt,
                generation_config={"temperature": 0.2, "max_output_tokens": 4096}
            )
            if response.text:
                partial_notes.append(response.text)
        except Exception as e:
            print(f"Warning: Chunk {idx} failed: {e}")
    return "\n\n".join(partial_notes).strip()