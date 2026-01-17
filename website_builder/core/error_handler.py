class WebsiteBuilderError(Exception):
    pass
class PromptValidationError(WebsiteBuilderError):
    pass
class GenerationError(WebsiteBuilderError):
    pass
class ValidationError(WebsiteBuilderError):
    pass
class ErrorHandler:
    @staticmethod
    def user_message(error: Exception) -> str:
        if isinstance(error, PromptValidationError):
            return "Prompt is too short or unclear."
        if isinstance(error, GenerationError):
            return "Website generation failed. Please try again."
        if isinstance(error, ValidationError):
            return "Generated website is invalid."
        return "Unexpected error occurred."