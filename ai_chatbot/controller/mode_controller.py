from ai_chatbot.llm.fast_model import FastModelClient
from ai_chatbot.llm.deep_model import DeepModelClient
from ai_chatbot.intelligence.prompt_builder import PromptBuilder
class ModeController:
    def __init__(self):
        self.fast_client = FastModelClient()
        self.deep_client = DeepModelClient()
    def run(self, mode: str, user_query: str, context: str) -> str:
        if mode == "DEEP":
            prompt = PromptBuilder.build_deep_prompt(user_query, context)
            return self.deep_client.run(prompt)
        prompt = PromptBuilder.build_fast_prompt(user_query, context)
        return self.fast_client.run(prompt)