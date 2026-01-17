class IntentClassifier:
    @staticmethod
    def classify(user_input: str) -> str:
        text = user_input.lower()
        if "resume" in text:
            return "RESUME_BUILD"
        if "website" in text:
            return "WEBSITE_BUILD"
        if "lecture" in text or "audio" in text:
            return "VOICE_NOTES"
        if "quiz" in text or "summarize" in text:
            return "STUDY_BUDDY"
        return "CHAT"