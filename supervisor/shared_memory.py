class SharedMemory:
    def __init__(self):
        self.reset()
    def reset(self):
        self.session_chat_history = []
        self.lecture_notes = None
        self.resume_data = None
        self.website_html = None
        self.user_profile = {
            "name": None,
            "role": None,
        }
        self.uploaded_pdf_path = None
        self.lecture_notes = None
    def add_chat(self, role: str, content: str):
        self.session_chat_history.append(
            {"role": role, "content": content}
        )
    def get_chat_context(self):
        return list(self.session_chat_history)
    def set_lecture_notes(self, notes: str):
        self.lecture_notes = notes
    def get_lecture_notes(self):
        return self.lecture_notes
    def set_resume(self, resume):
        self.resume_data = resume
    def get_resume(self):
        return self.resume_data
    def set_website(self, html: str):
        self.website_html = html
    def get_website(self):
        return self.website_html
    def set_uploaded_pdf(self, path: str):
        self.uploaded_pdf_path = path
    def get_uploaded_pdf(self):
        return self.uploaded_pdf_path
    def clear_uploaded_pdf(self):
        self.uploaded_pdf_path = None