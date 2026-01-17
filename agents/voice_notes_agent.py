from voice_to_notes_generator.state.lecture_state import lecture_state
from voice_to_notes_generator.pipelines.audio_ingestion import ingest_uploaded_audio
from voice_to_notes_generator.pipelines.transcription import transcribe_audio
from voice_to_notes_generator.pipelines.notes_generator import generate_structured_notes
from voice_to_notes_generator.pipelines.notes_qa import answer_from_notes
from utils.log_manager import LogManager
from utils.logger import log_agent_operation
import os
class VoiceNotesAgent:
    def __init__(self):
        self.state = lecture_state
        LogManager.info("VoiceNotesAgent initialized", agent="VOICE_NOTES")
        self.reset()
    @log_agent_operation("VOICE_NOTES", "reset_state")
    def reset(self):
        LogManager.info("Resetting VoiceNotesAgent state", agent="VOICE_NOTES")
        self.state = lecture_state
        self.state.audio_path = None
        self.state.transcript = None
        self.state.structured_notes = None
        LogManager.debug("VoiceNotesAgent state cleared", agent="VOICE_NOTES")
    @log_agent_operation("VOICE_NOTES", "set_audio")
    def set_audio(self, audio_path: str):
        LogManager.agent_start("VOICE_NOTES", "set_audio")
        if not audio_path:
            LogManager.error("Audio path cannot be empty", agent="VOICE_NOTES")
            raise ValueError("Audio path cannot be empty")
        if not os.path.exists(audio_path):
            LogManager.error(f"Audio file not found: {audio_path}", 
                            agent="VOICE_NOTES")
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        LogManager.file_operation("audio_upload", audio_path, "VOICE_NOTES",
                                 details={"file_size": os.path.getsize(audio_path)})
        self.state.set_audio(audio_path)
        LogManager.agent_end("VOICE_NOTES", "set_audio", "SUCCESS",
                           details={"audio_path": audio_path})
        LogManager.audit("audio_uploaded", 
                        details={"file": os.path.basename(audio_path),
                                 "path": audio_path})
    def has_audio(self) -> bool:
        has_audio = self.state.has_audio()
        LogManager.debug(f"has_audio check: {has_audio}", agent="VOICE_NOTES")
        return has_audio
    def has_transcript(self) -> bool:
        has_transcript = self.state.has_transcript()
        LogManager.debug(f"has_transcript check: {has_transcript}", 
                        agent="VOICE_NOTES")
        return has_transcript
    def has_notes(self) -> bool:
        has_notes = self.state.has_notes()
        LogManager.debug(f"has_notes check: {has_notes}", agent="VOICE_NOTES")
        return has_notes
    @log_agent_operation("VOICE_NOTES", "transcribe_audio")
    def transcribe(self):
        LogManager.info("Starting audio transcription", agent="VOICE_NOTES")        
        if not self.state.has_audio():
            LogManager.error("No audio file uploaded", agent="VOICE_NOTES")
            raise ValueError("No audio file uploaded. Please upload audio first.")
        audio_path = self.state.audio_path
        LogManager.file_operation("transcribe_audio", audio_path, "VOICE_NOTES",
                                 details={"audio_file": os.path.basename(audio_path)})       
        try:
            LogManager.agent_start("VOICE_NOTES", "transcription_process")
            transcript = transcribe_audio(audio_path)
            LogManager.agent_end("VOICE_NOTES", "transcription_process", "SUCCESS",
                               details={"transcript_length": len(transcript)})           
            self.state.set_transcript(transcript)            
            LogManager.info("Audio transcription completed", 
                           agent="VOICE_NOTES",
                           details={"audio_file": os.path.basename(audio_path),
                                    "transcript_chars": len(transcript)})
            LogManager.audit("audio_transcribed",
                           details={"file": os.path.basename(audio_path),
                                    "transcript_sample": transcript[:100]})            
            return transcript            
        except Exception as e:
            LogManager.agent_error("VOICE_NOTES", "transcription_process", e,
                                  details={"audio_path": audio_path})
            raise
    @log_agent_operation("VOICE_NOTES", "generate_notes")
    def generate_notes(self):
        LogManager.info("Generating structured notes from transcript", 
                       agent="VOICE_NOTES")
        if not self.state.has_transcript():
            LogManager.warning("No transcript available, transcribing first", 
                              agent="VOICE_NOTES")
            if not self.state.has_audio():
                LogManager.error("No audio or transcript available", 
                                agent="VOICE_NOTES")
                raise ValueError("No audio or transcript available. Please upload audio first.")
            self.transcribe()
        transcript = self.state.transcript
        LogManager.debug(f"Generating notes from transcript: {len(transcript)} chars", 
                        agent="VOICE_NOTES")
        try:
            LogManager.agent_start("VOICE_NOTES", "notes_generation")
            notes = generate_structured_notes(transcript)
            LogManager.agent_end("VOICE_NOTES", "notes_generation", "SUCCESS",
                               details={"notes_length": len(notes)})            
            self.state.set_notes(notes)           
            LogManager.info("Structured notes generated", 
                           agent="VOICE_NOTES",
                           details={"transcript_chars": len(transcript),
                                    "notes_chars": len(notes)})
            LogManager.audit("notes_generated",
                           details={"notes_sample": notes[:100]})           
            return notes           
        except Exception as e:
            LogManager.agent_error("VOICE_NOTES", "notes_generation", e,
                                  details={"transcript_length": len(transcript)})
            raise
    @log_agent_operation("VOICE_NOTES", "ask_from_notes")
    def ask_from_notes(self, question: str):
        LogManager.info(f"Question asked from notes: {question}", 
                       agent="VOICE_NOTES",
                       details={"question_length": len(question)})       
        if not self.state.has_notes():
            LogManager.error("No lecture notes available", agent="VOICE_NOTES")
            raise ValueError("No lecture notes available. Please generate notes first.")
        if not question or not question.strip():
            LogManager.error("Empty question received", agent="VOICE_NOTES")
            raise ValueError("Question cannot be empty.")
        LogManager.audit("notes_question_asked",
                        details={"question": question})       
        try:
            LogManager.agent_start("VOICE_NOTES", "notes_qa")
            answer = answer_from_notes(question)
            LogManager.agent_end("VOICE_NOTES", "notes_qa", "SUCCESS",
                               details={"answer_length": len(answer)})            
            LogManager.info("Question answered from notes", 
                           agent="VOICE_NOTES",
                           details={"question": question[:50],
                                    "answer_length": len(answer)})            
            return answer           
        except Exception as e:
            LogManager.agent_error("VOICE_NOTES", "notes_qa", e,
                                  details={"question": question})
            raise
    @log_agent_operation("VOICE_NOTES", "get_notes")
    def get_notes(self):
        if not self.state.has_notes():
            LogManager.debug("No notes available", agent="VOICE_NOTES")
            return None        
        notes = self.state.structured_notes
        LogManager.debug(f"Retrieved notes: {len(notes)} chars", 
                        agent="VOICE_NOTES")
        return notes
    def get_transcript(self):
        if not self.state.has_transcript():
            LogManager.debug("No transcript available", agent="VOICE_NOTES")
            return None        
        transcript = self.state.transcript
        LogManager.debug(f"Retrieved transcript: {len(transcript)} chars", 
                        agent="VOICE_NOTES")
        return transcript
    def get_audio_path(self):
        path = self.state.audio_path
        LogManager.debug(f"Retrieved audio path: {path}", agent="VOICE_NOTES")
        return path