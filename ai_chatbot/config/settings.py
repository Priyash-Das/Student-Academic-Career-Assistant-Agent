import os
from dotenv import load_dotenv
load_dotenv()
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 1))
MAX_CONTEXT_MESSAGES = int(os.getenv("MAX_CONTEXT_MESSAGES", 10))
DEFAULT_MODE = "FAST"
APP_TITLE = "Student Academic & Career Assistant Agent"
WINDOW_SIZE = "800x600"