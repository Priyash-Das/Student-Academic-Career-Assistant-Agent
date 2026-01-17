import os
from supervisor.intent_classifier import IntentClassifier
from supervisor.execution_router import ExecutionRouter
from supervisor.shared_memory import SharedMemory
from supervisor.adapters.chat_adapter import ChatAdapter
from agents.study_buddy_agent import StudyBuddyAgent
from agents.voice_notes_agent import VoiceNotesAgent
from agents.resume_agent import ResumeBuilderAgent
from agents.website_agent import WebsiteBuilderAgent
from utils.log_manager import LogManager
from utils.logger import log_agent_operation
class SupervisorAgent:
    def __init__(self):
        self.memory = SharedMemory()
        self.router = ExecutionRouter()
        LogManager.info("SupervisorAgent initialized", agent="SUPERVISOR")
        LogManager.agent_start("SUPERVISOR", "agent_initialization")
        self.chat_agent = ChatAdapter()
        self.study_buddy_agent = StudyBuddyAgent()
        self.voice_notes_agent = VoiceNotesAgent()
        self.resume_agent = ResumeBuilderAgent()
        self.website_agent = WebsiteBuilderAgent()
        LogManager.agent_end("SUPERVISOR", "agent_initialization", "SUCCESS",
                           details={"agents_initialized": 5})
        self.active_tool = "CHAT"
        LogManager.debug(f"Active tool set to: {self.active_tool}", agent="SUPERVISOR")
    @log_agent_operation("SUPERVISOR", "new_session")
    def new_session(self):
        LogManager.info("Starting new session", agent="SUPERVISOR")
        LogManager.audit("session_started")
        self.memory.reset()
        self.chat_agent.new_session()
        self.voice_notes_agent.reset()
        self.active_tool = "CHAT"
        LogManager.info("New session initialized", agent="SUPERVISOR",
                       details={"active_tool": self.active_tool})
    @log_agent_operation("SUPERVISOR", "set_active_tool")
    def set_active_tool(self, tool_key: str):
        previous_tool = self.active_tool
        self.active_tool = tool_key
        LogManager.info(f"Tool switched: {previous_tool} → {tool_key}", 
                       agent="SUPERVISOR")
        LogManager.audit("tool_switched",
                        details={"from": previous_tool, "to": tool_key})
        if tool_key == "VOICE_NOTES":
            LogManager.debug("Voice notes tool activated", agent="SUPERVISOR")
    def set_uploaded_file(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        self.memory.set_uploaded_pdf(file_path)
        return f"File uploaded: {os.path.basename(file_path)}"
    def upload_audio(self, audio_path: str):
        try:
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
            from voice_to_notes_generator.pipelines.audio_ingestion import ingest_uploaded_audio
            meta = ingest_uploaded_audio(audio_path)
            self.voice_notes_agent.set_audio(meta["audio_path"])
            return f"Audio uploaded successfully: {os.path.basename(audio_path)}"
        except Exception as e:
            raise Exception(f"Audio upload failed: {str(e)}")
    def get_website_html(self):
        html = self.memory.get_website()
        return html if html else None
    def live_preview_website(self):
        html = self.memory.get_website()
        if not html:
            return {"success": False, "message": "No website HTML available for preview."}
        try:
            from website_builder.preview.live_preview import LivePreview
            LivePreview.open(html)
            return {"success": True, "message": "Preview opened in browser."}
        except Exception as e:
            return {"success": False, "message": f"Preview failed: {str(e)}"}
    def copy_website_html(self):
        html = self.memory.get_website()
        if not html:
            return {"success": False, "message": "No website HTML available to copy.", "html": None}
        try:
            from website_builder.export.copy_manager import CopyManager
            CopyManager.copy(html)
            return {"success": True, "message": "HTML copied to clipboard.", "html": html}
        except Exception as e:
            return {"success": False, "message": f"Copy failed: {str(e)}", "html": None}
    def download_website_html_via_ui(self):
        html = self.memory.get_website()
        if not html:
            return {"success": False, "message": "No website HTML available to download.", "html": None}
        return {"success": True, "message": "Website ready for download.", "html": html}
    def handle_user_input(self, user_input: str, mode: str = "FAST"):
        intent = IntentClassifier.classify(user_input)
        if self.active_tool == "CHAT":
            response = self.chat_agent.run(
                user_query=user_input,
                mode=mode
            )
            self.memory.add_chat("user", user_input)
            self.memory.add_chat("assistant", response)
            return {
                "agent": "CHAT",
                "response": response
            }
        if self.active_tool == "STUDY_BUDDY":
            lowered = user_input.lower()
            if lowered.startswith("explain"):
                action = "EXPLAIN"
                content = user_input.replace("explain", "", 1).strip()
            elif lowered.startswith("summarize"):
                action = "SUMMARIZE"
                content = user_input.replace("summarize", "", 1).strip()
            elif lowered.startswith("quiz"):
                action = "QUIZ"
                content = user_input.replace("quiz", "", 1).strip()
            else:
                return {
                    "agent": "STUDY_BUDDY",
                    "response": (
                        "Please start your request with one of:\n"
                        "- explain\n- summarize\n- quiz"
                    )
                }
            try:
                result = self.study_buddy_agent.run(
                    action=action,
                    prompt=content,
                    pdf_path=self.memory.get_uploaded_pdf()
                )
                return {
                    "agent": "STUDY_BUDDY",
                    "response": result
                }
            except Exception as e:
                return {
                    "agent": "STUDY_BUDDY",
                    "response": f"Study Buddy error: {str(e)}"
                }
        if self.active_tool == "VOICE_NOTES":
            text = user_input.lower().strip()
            try:
                if text.startswith("upload audio"):
                    return {
                        "agent": "VOICE_NOTES",
                        "response": (
                            "Please use the Upload Audio button "
                            "(audio UI wiring comes next step)."
                        )
                    }
                if text.startswith("generate notes"):
                    notes = self.voice_notes_agent.generate_notes()
                    self.memory.set_lecture_notes(notes)
                    return {
                        "agent": "VOICE_NOTES",
                        "response": notes
                    }
                answer = self.voice_notes_agent.ask_from_notes(user_input)
                return {
                    "agent": "VOICE_NOTES",
                    "response": answer
                }
            except Exception as e:
                return {
                    "agent": "VOICE_NOTES",
                    "response": f"Voice-to-Notes error: {str(e)}"
                }
        if self.active_tool == "RESUME":
            data = {}
            for line in user_input.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    data[key.strip()] = value.strip()
            if not data:
                return {
                    "agent": "RESUME",
                    "response": (
                        "Please provide resume data in key:value format.\n\n"
                        "Example:\n"
                        "name: John Doe\n"
                        "skills: Python, SQL\n"
                        "education: BSc Computer Science"
                    )
                }
            try:
                result = self.resume_agent.build_resume(data)
                self.memory.set_resume(result)
                return {
                    "agent": "RESUME",
                    "response": (
                        "Resume generated successfully.\n\n"
                        f"{result['resume_text']}\n\n"
                        f"Saved to: {result['file_path']}"
                    )
                }
            except Exception as e:
                return {
                    "agent": "RESUME",
                    "response": f"Resume generation error: {str(e)}"
                }
        if self.active_tool == "WEBSITE":
            lines = user_input.splitlines()
            prompt = lines[0]
            modification = None
            if len(lines) > 1:
                modification = " ".join(lines[1:])
            try:
                html = self.website_agent.build(prompt, modification)
                self.memory.set_website(html)
                return {
                    "agent": "WEBSITE",
                    "response": (
                        "Website generated successfully.\n\n"
                        "HTML output stored in session.\n"
                        "Use Copy / Download / Live Preview buttons."
                    )
                }
            except Exception as e:
                return {
                    "agent": "WEBSITE",
                    "response": f"Website generation error: {str(e)}"
                }
        return {
            "agent": "UNKNOWN",
            "response": "Unknown tool context."
        }