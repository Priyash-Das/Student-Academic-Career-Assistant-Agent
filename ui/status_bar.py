import tkinter as tk
class StatusBar(tk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent, bg=colors["bg_main"], height=30)
        self.pack_propagate(False)
        tk.Frame(self, bg=colors["border"], height=1).pack(side=tk.TOP, fill=tk.X)
        self.label = tk.Label(
            self,
            text="Ready",
            anchor="w",
            bg=colors["bg_main"],
            fg=colors["text_secondary"],
            font=("Segoe UI", 9),
            padx=20
        )
        self.label.pack(side=tk.LEFT, fill=tk.Y)
    def set(self, text):
        self.label.config(text=text)