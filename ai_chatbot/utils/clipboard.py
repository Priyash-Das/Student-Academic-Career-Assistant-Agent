def copy_to_clipboard(root, text: str):
    if not text.strip():
        return
    root.clipboard_clear()
    root.clipboard_append(text)