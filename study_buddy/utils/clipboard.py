import tkinter as tk
def copy_to_clipboard(text: str):
    if not text:
        return
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    root.destroy()