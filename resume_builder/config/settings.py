import os
import sys
from dotenv import load_dotenv
load_dotenv()
APP_NAME = "AI-Powered Resume Builder"
APP_VERSION = "1.0.0"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("ERROR: GROQ_API_KEY is missing in .env file")
    print("Please add: GROQ_API_KEY=your_api_key_here")
    sys.exit(1)
DEMO_MODE = True
MAX_RESUME_LENGTH = 2000
ALLOWED_FILE_EXTENSIONS = ['.docx']