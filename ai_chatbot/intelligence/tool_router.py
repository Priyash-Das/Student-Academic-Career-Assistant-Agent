from typing import Dict
class ToolRouter:
    TOOL_PRIORITY = {
        "SYSTEM_TIME": 100,
        "WEB": 90,
        "LLM": 10,
    }
    @classmethod
    def route(cls, classification: Dict[str, any]) -> Dict[str, any]:
        intent = classification.get("intent")
        confidence = classification.get("confidence", 1.0)
        freshness = classification.get("freshness")
        if intent == "system_time":
            return cls._decision(
                tool="SYSTEM_TIME",
                reason="System time query",
                allow_llm=False,
            )
        if freshness == "real_time" and intent in ["news", "real_time_factual"]:
            return cls._decision(
                tool="WEB",
                reason="Real-time information required",
                allow_llm=False,
            )
        if confidence < 0.5:
            return cls._decision(
                tool="LLM",
                reason="Low classification confidence",
                allow_llm=True,
            )
        return cls._decision(
            tool="LLM",
            reason="Static or reasoning query",
            allow_llm=True,
        )
    @staticmethod
    def _decision(tool: str, reason: str, allow_llm: bool) -> Dict[str, any]:
        return {
            "tool": tool,
            "allow_llm": allow_llm,
            "reason": reason,
            "priority": ToolRouter.TOOL_PRIORITY.get(tool, 0),
        }