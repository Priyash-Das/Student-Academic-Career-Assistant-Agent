import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
TEMP_AUDIO_DIR = BASE_DIR / "assets" / "temp_audio"
TEMP_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
SUPPORTED_AUDIO_FORMATS = {".wav", ".mp3", ".m4a"}
TRANSCRIPT_CHUNK_SIZE = 1200
NOTES_CHUNK_SIZE = 1500
QA_MAX_TOKENS = 512
STRICT_QA_FALLBACK_MESSAGE = (
    "This information is not available in the provided lecture notes."
)