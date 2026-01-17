import os
from dotenv import load_dotenv
load_dotenv()
CHATBOT_DEFAULT = os.getenv("CHATBOT_DEFAULT")
CHATBOT_DEEP = os.getenv("CHATBOT_DEEP")
CHATBOT_FALLBACK = os.getenv("CHATBOT_FALLBACK")