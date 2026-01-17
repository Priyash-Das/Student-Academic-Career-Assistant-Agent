from typing import Dict, List
class QueryClassifier:
    INTENT_RULES = {
        "system_time": {
            "keywords": [
                "time", "date", "current time", "current date", "today date"
            ],
            "priority": 100,
            "freshness": "real_time",
            "complexity": "shallow",
            "mode": "FAST",
        },
        "news": {
            "keywords": [
                "news", "latest", "headlines", "breaking", "updates"
            ],
            "priority": 90,
            "freshness": "real_time",
            "complexity": "shallow",
            "mode": "FAST",
        },
        "real_time_factual": {
            "keywords": [
                "pm", "prime minister", "president", "ceo",
                "price", "weather", "temperature", "stock"
            ],
            "priority": 80,
            "freshness": "real_time",
            "complexity": "shallow",
            "mode": "FAST",
        },
        "coding": {
            "keywords": [
                "code", "error", "exception", "bug", "debug",
                "stack trace", "python", "java", "c++"
            ],
            "priority": 70,
            "freshness": "static",
            "complexity": "deep",
            "mode": "DEEP",
        },
        "deep_reasoning": {
            "keywords": [
                "explain", "why", "how", "step by step",
                "analyze", "compare", "design", "architecture"
            ],
            "priority": 60,
            "freshness": "static",
            "complexity": "deep",
            "mode": "DEEP",
        },
    }
    @staticmethod
    def _score_intent(query: str, keywords: List[str]) -> int:
        score = 0
        for kw in keywords:
            if kw in query:
                score += 1
        return score
    @classmethod
    def classify(cls, query: str) -> Dict[str, str]:
        q = query.lower()
        matches = []
        for intent, rule in cls.INTENT_RULES.items():
            score = cls._score_intent(q, rule["keywords"])
            if score > 0:
                matches.append({
                    "intent": intent,
                    "score": score,
                    "priority": rule["priority"],
                    **rule
                })
        if not matches:
            return {
                "intent": "general",
                "complexity": "shallow",
                "freshness": "static",
                "recommended_mode": "FAST",
                "confidence": 0.2,
                "reason": "No rule matched"
            }
        matches.sort(
            key=lambda x: (x["priority"], x["score"]),
            reverse=True
        )
        top = matches[0]
        confidence = min(1.0, 0.3 + (0.2 * top["score"]))
        return {
            "intent": top["intent"],
            "complexity": top["complexity"],
            "freshness": top["freshness"],
            "recommended_mode": top["mode"],
            "confidence": round(confidence, 2),
            "reason": f"Matched keywords with priority {top['priority']}"
        }