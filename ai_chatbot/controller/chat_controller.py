from ai_chatbot.controller.mode_controller import ModeController
from ai_chatbot.controller.fallback_controller import FallbackController
from ai_chatbot.controller.session_manager import SessionManager
from ai_chatbot.intelligence.query_classifier import QueryClassifier
from ai_chatbot.intelligence.tool_router import ToolRouter
from ai_chatbot.intelligence.system_tools import SystemTools
from ai_chatbot.intelligence.web_search import WebSearch
from ai_chatbot.intelligence.web_summarizer import WebSummarizer
from ai_chatbot.utils.error_handler import ErrorHandler
class ChatController:
    def __init__(self):
        self.mode_controller = ModeController()
        self.fallback_controller = FallbackController()
        self.session_manager = SessionManager()
        self.web_summarizer = WebSummarizer()
    def new_chat(self):
        self.session_manager.new_session()
    def process(self, user_query: str, mode: str) -> str:
        context_manager = self.session_manager.get_context_manager()
        context_manager.add_user_message(user_query)
        context = context_manager.get_context()
        classification = QueryClassifier.classify(user_query)
        auto_mode = classification.get("recommended_mode", "FAST")
        final_mode = mode if mode else auto_mode
        decision = ToolRouter.route(classification)
        tool = decision["tool"]
        allow_llm = decision["allow_llm"]
        try:
            if tool == "SYSTEM_TIME":
                response = SystemTools.current_datetime()
                context_manager.add_assistant_message(response)
                return response
            if tool == "WEB" and not allow_llm:
                web_result = WebSearch.run(user_query)
                summarized = self.web_summarizer.summarize(web_result)
                response = (
                    "This answer is based on real-time web data:\n\n"
                    f"{summarized}"
                )
                context_manager.add_assistant_message(response)
                return response
            if tool == "WEB" and allow_llm:
                web_result = WebSearch.run(user_query)
                summarized = self.web_summarizer.summarize(web_result)
                context += f"\n[Web Result]\n{web_result}"
            response = self.mode_controller.run(
                mode=final_mode,
                user_query=user_query,
                context=context,
            )
        except Exception as primary_error:
            try:
                response = self.fallback_controller.run(context)
            except Exception as fallback_error:
                return ErrorHandler.handle(fallback_error)
        context_manager.add_assistant_message(response)
        return response