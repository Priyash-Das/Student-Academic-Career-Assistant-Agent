import tkinter as tk
class Header(tk.Frame):
    def __init__(self, parent, on_mode_change, colors):
        super().__init__(parent, bg=colors["bg_main"], height=60)
        self.pack_propagate(False)
        self.colors = colors
        toggle_frame = tk.Frame(self, bg=colors["bg_main"])
        toggle_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        tk.Label(
            toggle_frame,
            text="Model:",
            font=("Segoe UI", 10, "bold"),
            bg=colors["bg_main"],
            fg=colors["text_secondary"]
        ).pack(side=tk.LEFT, padx=5)
        self.mode = tk.StringVar(value="FAST")
        for m in ("FAST", "DEEP"):
            rb = tk.Radiobutton(
                toggle_frame,
                text=m,
                variable=self.mode,
                value=m,
                bg=colors["bg_main"],
                activebackground=colors["bg_main"],
                font=("Segoe UI", 9),
                command=lambda: on_mode_change(self.mode.get()),
                selectcolor=colors["bg_main"]
            )
            rb.pack(side=tk.LEFT, padx=2)
        tk.Frame(self, bg=colors["border"], height=1).pack(side=tk.BOTTOM, fill=tk.X)