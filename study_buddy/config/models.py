import os
from dotenv import load_dotenv
load_dotenv()
STUDY_READER_MODEL = os.getenv("STUDY_READER_MODEL")
STUDY_EXPLAIN_MODEL = os.getenv("STUDY_EXPLAIN_MODEL")
STUDY_SUMMARY_MODEL = os.getenv("STUDY_SUMMARY_MODEL")
STUDY_QUIZ_MODEL = os.getenv("STUDY_QUIZ_MODEL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")
if not all([
    STUDY_READER_MODEL,
    STUDY_EXPLAIN_MODEL,
    STUDY_SUMMARY_MODEL,
    STUDY_QUIZ_MODEL,
]):
    raise RuntimeError("One or more STUDY_BUDDY model variables are missing.")
if not any([GOOGLE_API_KEY, GROQ_API_KEY, HF_API_KEY]):
    raise RuntimeError("At least one API key must be provided.")