from ai_chatbot.controller.chat_controller import ChatController
class ChatAdapter:
    def __init__(self):
        self.controller = ChatController()
    def new_session(self):
        self.controller.new_chat()
    def run(self, user_query: str, mode: str = "FAST") -> str:
        return self.controller.process(user_query, mode)