class PromptProcessor:
    def __init__(self, base_prompt: str, modification: str | None = None):
        self.base_prompt = base_prompt or ""
        self.modification = modification or ""
    def normalize(self) -> str:
        text = self.base_prompt.strip()
        text = " ".join(text.split())
        return text
    def merge(self) -> str:
        base = self.normalize()
        if self.modification:
            mod = " ".join(self.modification.strip().split())
            return f"{base}. Modification request: {mod}"
        return base
    def is_valid(self) -> bool:
        return len(self.normalize()) > 10