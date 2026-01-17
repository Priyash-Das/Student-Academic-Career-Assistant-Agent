import json
import random
from study_buddy.llm.client import call_llm
from study_buddy.llm.prompts import STRUCTURED_QUIZ_PROMPT
from study_buddy.config.models import STUDY_QUIZ_MODEL
from study_buddy.utils.errors import PipelineError
def generate_quiz(study_context: str) -> dict:
    prompt = STRUCTURED_QUIZ_PROMPT.format(study_context=study_context)
    raw = call_llm(STUDY_QUIZ_MODEL, prompt)
    try:
        cleaned = raw.strip()
        if "```" in cleaned:
            cleaned = cleaned.replace("```json", "")
            cleaned = cleaned.replace("```", "")
            cleaned = cleaned.strip()
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1:
            raise ValueError("No JSON object found in model output")
        json_text = cleaned[start:end + 1]
        data = json.loads(json_text)
        questions = data.get("questions", [])
        if len(questions) != 10:
            raise ValueError(f"Expected 10 questions, got {len(questions)}")
        return data
    except Exception as e:
        print("\n[QUIZ PARSE ERROR]")
        print(raw)
        raise PipelineError(
            "Quiz generation failed due to invalid model output. "
            "See terminal for details."
        )
def normalize_question(question: dict) -> dict:
    options = question["options"]
    correct_key = question["correct"]
    items = list(options.items())
    correct_text = options[correct_key]
    random.shuffle(items)
    new_options = {}
    new_correct = None
    labels = ["A", "B", "C", "D"]
    for label, (old_key, text) in zip(labels, items):
        new_options[label] = text
        if text == correct_text:
            new_correct = label
    return {
        "question": question["question"],
        "options": new_options,
        "correct": new_correct
    }