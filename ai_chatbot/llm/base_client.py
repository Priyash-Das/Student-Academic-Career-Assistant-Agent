import os
import time
import json
import requests
from ai_chatbot.config.settings import MAX_RETRIES, REQUEST_TIMEOUT
class LLMError(Exception):
    pass
class BaseLLMClient:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.api_key = self._resolve_api_key()
        self.endpoint = self._resolve_endpoint()
    def _resolve_api_key(self) -> str:
        if "gemini" in self.model_name:
            return os.getenv("GOOGLE_API_KEY")
        if "llama" in self.model_name:
            return os.getenv("GROQ_API_KEY")
        return os.getenv("HF_API_KEY")
    def _resolve_endpoint(self) -> str:
        if "gemini" in self.model_name:
            return "https://generativelanguage.googleapis.com/v1beta/models"
        if "llama" in self.model_name:
            return "https://api.groq.com/openai/v1/chat/completions"
        return "https://api-inference.huggingface.co/models"
    def generate(self, prompt: str) -> str:
        if "gemini" in self.model_name:
            return self._generate_gemini(prompt)
        if "llama" in self.model_name:
            return self._generate_groq(prompt)
        return self._generate_huggingface(prompt)
    def _generate_gemini(self, prompt: str) -> str:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model_name}:generateContent?key={self.api_key}"
        )
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        response = requests.post(
            url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code != 200:
            raise Exception(response.text)
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    def _generate_groq(self, prompt: str) -> str:
        url = "https://api.groq.com/openai/v1/chat/completions"
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()["choices"][0]["message"]["content"].strip()
    def _generate_huggingface(self, prompt: str) -> str:
        url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={"inputs": prompt},
            timeout=REQUEST_TIMEOUT,
        )
        if response.status_code != 200:
            raise Exception(response.text)
        return response.json()[0]["generated_text"].strip()