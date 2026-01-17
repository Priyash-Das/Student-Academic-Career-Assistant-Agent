from resume_builder.llm.groq_client import GroqClient
from resume_builder.config.prompts import BASE_RESUME_SYSTEM_PROMPT
class LLMRouter:
    @staticmethod
    def generate_resume(user_prompt: str) -> str:
        return GroqClient.generate(
            system_prompt=BASE_RESUME_SYSTEM_PROMPT,
            user_content=user_prompt
        )
    @staticmethod
    def assist_edit(system_prompt: str, content: str) -> str:
        return GroqClient.generate(
            system_prompt=system_prompt,
            user_content=content
        )