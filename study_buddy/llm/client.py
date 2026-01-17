import time
import requests
from study_buddy.config.models import (
    GOOGLE_API_KEY,
    GROQ_API_KEY,
    HF_API_KEY,
)
from study_buddy.config.settings import MAX_LLM_RETRIES, LLM_TIMEOUT_SECONDS
from study_buddy.utils.errors import LLMCallError
def call_llm(model: str, prompt: str) -> str:
    for attempt in range(MAX_LLM_RETRIES):
        try:
            if model.startswith("gemini"):
                return _call_gemini(model, prompt)
            if model.startswith("llama"):
                return _call_groq(model, prompt)
            if "/" in model:
                return _call_huggingface(model, prompt)
            raise LLMCallError(f"Unsupported model: {model}")
        except Exception as e:
            if attempt == MAX_LLM_RETRIES - 1:
                raise LLMCallError("LLM request failed.") from e
            time.sleep(1)
def _call_gemini(model: str, prompt: str) -> str:
    if not GOOGLE_API_KEY:
        raise LLMCallError("Google API key missing.")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(
        url,
        params={"key": GOOGLE_API_KEY},
        json=payload,
        timeout=LLM_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    data = response.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]
def _call_groq(model: str, prompt: str) -> str:
    if not GROQ_API_KEY:
        raise LLMCallError("Groq API key missing.")
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=LLM_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
def _call_huggingface(model: str, prompt: str) -> str:
    if not HF_API_KEY:
        raise LLMCallError("HuggingFace API key missing.")
    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"inputs": prompt}
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=LLM_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    data = response.json()
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and "generated_text" in item:
                return item["generated_text"]
        return ""
    if isinstance(data, dict):
        return data.get("generated_text", "")
    return ""