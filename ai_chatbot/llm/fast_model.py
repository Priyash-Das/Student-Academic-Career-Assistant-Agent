from ai_chatbot.llm.base_client import BaseLLMClient
from ai_chatbot.config.models import CHATBOT_DEFAULT
class FastModelClient:
    def __init__(self):
        self.client = BaseLLMClient(CHATBOT_DEFAULT)
    def run(self, prompt: str) -> str:
        return self.client.generate(prompt)