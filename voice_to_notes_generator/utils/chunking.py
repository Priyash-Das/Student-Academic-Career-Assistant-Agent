def chunk_text(text: str, max_size: int):
    words = text.split()
    chunks = []
    current = []
    for word in words:
        current.append(word)
        if len(current) >= max_size:
            chunks.append(" ".join(current))
            current = []
    if current:
        chunks.append(" ".join(current))
    return chunks