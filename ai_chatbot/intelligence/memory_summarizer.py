class MemorySummarizer:
    @staticmethod
    def summarize(messages: list) -> str:
        if not messages:
            return ""
        summary_lines = []
        for msg in messages:
            if msg.startswith("User:"):
                summary_lines.append(f"- User asked about {msg[5:50]}...")
            elif msg.startswith("Assistant:"):
                summary_lines.append(f"- Assistant responded with guidance.")
        return "Conversation Summary:\n" + "\n".join(summary_lines[:5])