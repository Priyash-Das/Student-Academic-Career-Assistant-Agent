class HealthCheck:
    @staticmethod
    def run(html: str | None) -> bool:
        if not html:
            return False
        checks = {
            "<html": "<html missing",
            "</html>": "</html> missing",
            "<body": "<body missing",
        }
        lower = html.lower()
        for key, msg in checks.items():
            if key not in lower:
                return False
        return True