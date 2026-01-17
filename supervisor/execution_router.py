class ExecutionRouter:
    TOOL_CONTEXTS = {
        "Main Chat": "CHAT",
        "Study Buddy": "STUDY_BUDDY",
        "Voice-to-Notes": "VOICE_NOTES",
        "Resume Builder": "RESUME",
        "Website Builder": "WEBSITE",
    }
    def resolve_context(self, selected_tool: str) -> str:
        return self.TOOL_CONTEXTS.get(selected_tool, "CHAT")