import os
import requests
class WebSearch:
    SERPAPI_ENDPOINT = "https://serpapi.com/search.json"
    @staticmethod
    def run(query: str) -> str:
        api_key = os.getenv("SERPAPI_KEY")
        if not api_key:
            return "Web search unavailable (SERPAPI_KEY missing)."
        params = {
            "q": query,
            "engine": "google",
            "api_key": api_key,
            "num": 6,
        }
        try:
            response = requests.get(
                WebSearch.SERPAPI_ENDPOINT,
                params=params,
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
        except Exception:
            return "Failed to retrieve real-time information."
        results = data.get("organic_results", [])
        if not results:
            return "No reliable real-time results found."
        q = query.lower()
        if any(w in q for w in ["weather", "temperature", "rain", "forecast"]):
            return WebSearch._format_weather(results)
        if any(w in q for w in ["news", "latest", "headlines"]):
            return WebSearch._format_news(results)
        return WebSearch._format_factual(results)
    @staticmethod
    def _format_weather(results):
        for r in results:
            snippet = r.get("snippet", "")
            link = r.get("link", "")
            if snippet:
                return (
                    "🌦 **Current Weather Information**\n\n"
                    f"{snippet}\n\n"
                    f"Source: {link}"
                )
        return "Weather data found, but could not extract current conditions."
    @staticmethod
    def _format_news(results):
        lines = ["📰 **Latest News (Top Sources)**\n"]
        for r in results[:4]:
            title = r.get("title", "")
            snippet = r.get("snippet", "")
            link = r.get("link", "")
            lines.append(f"- **{title}**\n  {snippet}\n  {link}\n")
        return "\n".join(lines)
    @staticmethod
    def _format_factual(results):
        best = results[0]
        return (
            "ℹ️ **Real-Time Information**\n\n"
            f"{best.get('snippet', '')}\n\n"
            f"Source: {best.get('link', '')}"
        )