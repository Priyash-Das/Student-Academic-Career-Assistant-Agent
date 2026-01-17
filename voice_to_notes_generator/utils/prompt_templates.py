def lecture_notes_prompt(transcript: str) -> str:
    return f"""
You are an academic note-generation system.

STRICT RULES:
- Use ONLY the provided lecture transcript.
- Do NOT add examples, explanations, or facts not explicitly stated.
- Do NOT invent formulas, definitions, or terminology.
- Remove filler words, repetitions, and verbal noise.
- Preserve emphasis and ordering from the lecturer.
- Academic tone only.

OUTPUT FORMAT (MANDATORY):
Title
Overview
Key Concepts
Detailed Explanations
Important Definitions
Examples (ONLY if present)
Formulas / Code (ONLY if present)
Key Takeaways
Revision Checklist

LECTURE TRANSCRIPT:
\"\"\"
{transcript}
\"\"\"
"""
def notes_qa_prompt(notes: str, question: str) -> str:
    return f"""
You are answering questions strictly from lecture notes.

RULES:
- Use ONLY the provided notes.
- Do NOT use external knowledge.
- Do NOT infer or guess.
- If the answer is missing, reply EXACTLY:
"This information is not available in the provided lecture notes."

LECTURE NOTES:
\"\"\"
{notes}
\"\"\"

QUESTION:
{question}
"""
def explain_answer_prompt(notes: str, answer: str) -> str:
    return f"""
You are an academic tutor.

TASK:
Explain the given answer in a way that is EASY to understand for a beginner.

RULES:
- Stay within the scope of the lecture notes.
- Use simple, clear language.
- Break the explanation into short paragraphs.
- You MAY use examples for clarity.
- ALWAYS include at least ONE example.
- Examples must be relevant to daily life or simple scenarios.
- Do NOT introduce external facts.
- Do NOT contradict the original answer.
- Do NOT add advanced theory not present in the notes.

LECTURE NOTES:
\"\"\"
{notes}
\"\"\"

ORIGINAL ANSWER:
\"\"\"
{answer}
\"\"\"

OUTPUT FORMAT:
- Simple explanation
- Example (clearly labeled)

Now provide a clearer, more detailed explanation for a student.
"""