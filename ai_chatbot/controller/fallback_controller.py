from ai_chatbot.llm.fast_model import FastModelClient
from ai_chatbot.llm.deep_model import DeepModelClient
from ai_chatbot.llm.fallback_model import FallbackModelClient
class FallbackController:
    def __init__(self):
        self.fast = FastModelClient()
        self.deep = DeepModelClient()
        self.fallback = FallbackModelClient()
    def run(self, prompt: str) -> str:
        try:
            return self.fast.run(prompt)
        except Exception as e:
            try:
                return self.deep.run(prompt)
            except Exception as e:
                try:
                    return self.fallback.run(prompt)
                except Exception as e:
                    raise e