from collections import deque
from ai_chatbot.intelligence.memory_summarizer import MemorySummarizer
from ai_chatbot.config.settings import MAX_CONTEXT_MESSAGES
class ContextManager:
    def __init__(self):
        self.messages = deque()
        self.summary_memory = ""
    def add_user_message(self, message: str):
        self.messages.append(f"User: {message}")
    def add_assistant_message(self, message: str):
        self.messages.append(f"Assistant: {message}")
        self._trim_if_needed()
    def _trim_if_needed(self):
        if len(self.messages) <= MAX_CONTEXT_MESSAGES:
            return
        old_messages = list(self.messages)[: len(self.messages) // 2]
        self.summary_memory = MemorySummarizer.summarize(old_messages)
        self.messages = deque(
            list(self.messages)[len(self.messages) // 2 :]
        )
    def get_context(self) -> str:
        parts = []
        if self.summary_memory:
            parts.append(self.summary_memory)
        parts.extend(self.messages)
        return "\n".join(parts)
    def clear(self):
        self.messages.clear()
        self.summary_memory = ""