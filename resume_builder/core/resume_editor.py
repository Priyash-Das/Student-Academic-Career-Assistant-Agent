from resume_builder.config.prompts import EDITOR_ASSIST_PROMPT
from resume_builder.llm.llm_router import LLMRouter
class ResumeEditor:
    @staticmethod
    def improve_text(text: str) -> str:
        if not text or not text.strip():
            return text
        improved = LLMRouter.assist_edit(
            system_prompt=EDITOR_ASSIST_PROMPT,
            content=text.strip()
        )
        return improved.strip()
    @staticmethod
    def improve_bullets(bullets: list[str]) -> list[str]:
        if not bullets:
            return bullets
        joined = "\n".join(f"- {b}" for b in bullets)
        improved = LLMRouter.assist_edit(
            system_prompt=EDITOR_ASSIST_PROMPT,
            content=joined
        )
        lines = []
        for line in improved.splitlines():
            clean = line.lstrip("- ").strip()
            if clean:
                lines.append(clean)
        return lines