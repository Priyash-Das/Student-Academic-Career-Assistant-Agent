import shutil
import uuid
from pathlib import Path
from voice_to_notes_generator.config.settings import TEMP_AUDIO_DIR, SUPPORTED_AUDIO_FORMATS
class AudioIngestionError(Exception):
    pass
def ingest_uploaded_audio(file_path: str) -> dict:
    src = Path(file_path)
    if not src.exists():
        raise AudioIngestionError("Audio file does not exist.")
    if src.suffix.lower() not in SUPPORTED_AUDIO_FORMATS:
        raise AudioIngestionError(
            "Unsupported audio format. Only WAV, MP3, and M4A are supported."
        )
    dest_name = f"{uuid.uuid4().hex}{src.suffix.lower()}"
    dest_path = TEMP_AUDIO_DIR / dest_name
    shutil.copy(src, dest_path)
    return {
        "audio_path": str(dest_path),
        "format": src.suffix.lower(),
        "source": "upload",
    }