from typing import List
from study_buddy.config.settings import (
    CHUNK_SIZE_CHARS,
    CHUNK_OVERLAP_CHARS,
    MAX_CONTEXT_CHUNKS,
)
def chunk_text(text: str) -> List[str]:
    if not text:
        return []
    chunks: List[str] = []
    start = 0
    length = len(text)
    while start < length:
        end = start + CHUNK_SIZE_CHARS
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk.strip())
        if len(chunks) >= MAX_CONTEXT_CHUNKS:
            break
        start = end - CHUNK_OVERLAP_CHARS
        if start < 0:
            start = 0
    return chunks