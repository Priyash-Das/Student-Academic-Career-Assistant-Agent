from ai_chatbot.llm.fast_model import FastModelClient
class WebSummarizer:
    def __init__(self):
        self.client = FastModelClient()
    def summarize(self, web_text: str) -> str:
        prompt = f"""
[SYSTEM]
You are a summarization engine.

Rules:
- ONLY summarize the information provided below.
- DO NOT add new facts.
- DO NOT guess or infer missing information.
- If the information is unclear, say so.
- Keep the answer concise and factual.

[WEB DATA]
{web_text}

[SUMMARY]
""".strip()
        try:
            return self.client.run(prompt)
        except Exception:
            return web_text