from ai_chatbot.intelligence.context_manager import ContextManager
class SessionManager:
    def __init__(self):
        self.context_manager = ContextManager()
    def new_session(self):
        self.context_manager.clear()
    def get_context_manager(self) -> ContextManager:
        return self.context_manager