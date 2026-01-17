from typing import Optional
from datetime import datetime
class LectureState:
    def __init__(self):
        self.reset()
    def reset(self):
        self.audio_path: Optional[str] = None
        self.transcript: Optional[str] = None
        self.structured_notes: Optional[str] = None
        self.created_at: Optional[datetime] = None
    def set_audio(self, audio_path: str):
        self.audio_path = audio_path
        self.transcript = None
        self.structured_notes = None
        self.created_at = None
    def set_transcript(self, transcript: str):
        if not transcript or not transcript.strip():
            raise ValueError("Transcript cannot be empty.")
        self.transcript = transcript
    def set_notes(self, notes: str):
        if not notes or not notes.strip():
            raise ValueError("Structured notes cannot be empty.")
        self.structured_notes = notes
        self.created_at = datetime.utcnow()
    def has_audio(self) -> bool:
        return self.audio_path is not None
    def has_transcript(self) -> bool:
        return self.transcript is not None
    def has_notes(self) -> bool:
        return self.structured_notes is not None
    def get_notes_for_qa(self) -> str:
        if not self.structured_notes:
            raise RuntimeError("No lecture notes available for Q&A.")
        return self.structured_notes
lecture_state = LectureState()