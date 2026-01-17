class ErrorHandler:
    @staticmethod
    def handle(error: Exception) -> str:
        return (
            "Something went wrong while processing your request. "
            "Please try again."
        )