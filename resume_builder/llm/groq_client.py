import requests
from resume_builder.config.settings import GROQ_API_KEY
from resume_builder.config.models import EDITOR_ASSIST_MODEL
class GroqClient:
    BASE_URL = "https://api.groq.com/openai/v1/chat/completions"
    @classmethod
    def generate(cls, system_prompt: str, user_content: str) -> str:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": EDITOR_ASSIST_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.3
        }
        response = requests.post(cls.BASE_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError):
            raise RuntimeError("Invalid response from Groq API")