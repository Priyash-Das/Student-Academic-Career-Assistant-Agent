import re
class HTMLValidator:
    REQUIRED_TAGS = ["<html", "</html>", "<head", "</head>", "<body", "</body>"]
    @classmethod
    def is_valid(cls, html: str) -> bool:
        if not html:
            return False
        lower = html.lower()
        required = ["<html", "<head", "<body", "</html>"]
        for tag in required:
            if tag not in lower:
                return False
        if re.search(r"<script\s+[^>]*src\s*=", lower):
            return False
        if "<link" in lower and "href=" in lower:
            return False
        return True