import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()
class LLMClient:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        if not self.groq_key:
            raise RuntimeError("GROQ_API_KEY missing")
        self.client = Groq(api_key=self.groq_key)
        self.model = os.getenv(
            "WEBSITE_MODEL",
            "llama-3.3-70b-versatile"
        )
    def generate(self, model: str, prompt: str):
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You generate ONLY valid HTML. No explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.4,
            max_tokens=6000,
        )
        content = completion.choices[0].message.content
        if not content:
            raise RuntimeError("Empty Groq response")
        return {
            "html": content
        }