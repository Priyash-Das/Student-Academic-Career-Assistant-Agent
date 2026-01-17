import os
TRANSCRIBE_MODEL = os.getenv("TRANSCRIBE_MODEL", "whisper-large-v3")
LECTURE_NOTES_MODEL = os.getenv("LECTURE_NOTES_MODEL", "gemini-2.5-flash")
NOTES_QA_MODEL = os.getenv("NOTES_QA_MODEL", "llama-3.3-70b-versatile")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
def validate_keys():
    google_key = os.getenv("GOOGLE_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    missing = []
    if not google_key:
        missing.append("GOOGLE_API_KEY")
    if not groq_key:
        missing.append("GROQ_API_KEY")
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}"
        )