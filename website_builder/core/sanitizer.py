import re
class OutputSanitizer:
    @staticmethod
    def sanitize(raw_output: str) -> str:
        if not raw_output:
            return ""
        text = raw_output.strip()
        text = re.sub(r"`{3,}", "", text)
        text = text.replace("```html", "").replace("```", "").strip()
        text = re.sub(r"```html", "", text, flags=re.IGNORECASE)
        text = re.sub(r"```", "", text)
        if "<html" not in text.lower():
            return ""
        start = text.lower().find("<html")
        end = text.lower().rfind("</html>")
        if end == -1:
            text += "\n</body>\n</html>"
            end = text.lower().rfind("</html>")
        clean = text[start:end + 7].strip()
        return clean