import tkinter as tk
class CopyManager:
    @staticmethod
    def copy(html: str):
        root = tk.Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(html)
        root.update()
        root.destroy()