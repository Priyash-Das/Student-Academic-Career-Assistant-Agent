from pathlib import Path
from voice_to_notes_generator.config.models import GROQ_API_KEY, TRANSCRIBE_MODEL
class TranscriptionError(Exception):
    pass
def transcribe_audio(audio_path: str) -> str:
    path = Path(audio_path)
    if not path.exists():
        raise TranscriptionError("Audio file not found.")
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        with open(path, "rb") as audio_file:
            response = client.audio.transcriptions.create(
                file=audio_file,
                model=TRANSCRIBE_MODEL,
                response_format="text",
            )
        if not response or not response.strip():
            raise TranscriptionError("Empty transcription received.")
        return response.strip()
    except Exception as e:
        raise TranscriptionError(f"Whisper transcription failed: {e}")