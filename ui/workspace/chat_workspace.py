import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from ui.workspace.base import BaseWorkspace
class ChatWorkspace(BaseWorkspace):
    def __init__(self, parent, supervisor, get_mode, colors):
        super().__init__(parent, supervisor, colors)
        self.get_mode = get_mode
        center_frame = tk.Frame(self, bg=self.colors["bg_main"])
        center_frame.pack(fill=tk.BOTH, expand=True, padx=0)
        self.output = ScrolledText(
            center_frame,
            state=tk.DISABLED,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg=self.colors["bg_main"],
            fg=self.colors["text_primary"],
            bd=0,
            padx=20,
            pady=20,
            highlightthickness=0
        )
        self.output.pack(fill=tk.BOTH, expand=True)
        self.output.tag_config("user_label", foreground=self.colors["text_primary"], font=("Segoe UI", 10, "bold"), spacing1=20, spacing3=5)
        self.output.tag_config("user_msg", foreground=self.colors["text_primary"], background="#F7F7F8", font=("Segoe UI", 11), lmargin1=20, lmargin2=20, rmargin=20, spacing1=10, spacing3=10)
        self.output.tag_config("agent_label", foreground=self.colors["accent"], font=("Segoe UI", 10, "bold"), spacing1=20, spacing3=5)
        self.output.tag_config("agent_msg", foreground=self.colors["text_primary"], font=("Segoe UI", 11), lmargin1=20, lmargin2=20, rmargin=20, spacing1=10, spacing3=10)
        self.output.tag_config("divider", font=("Arial", 4))
        input_container = tk.Frame(self, bg=self.colors["bg_main"])
        input_container.pack(fill=tk.X, side=tk.BOTTOM, pady=20)
        input_frame = tk.Frame(input_container, bg="white", bd=1, relief=tk.SOLID)
        input_frame.config(highlightbackground=self.colors["border"], highlightthickness=1, bd=0)
        input_frame.pack(fill=tk.X, padx=40, ipadx=5, ipady=5)
        self.input = tk.Entry(
            input_frame, 
            font=("Segoe UI", 12),
            bd=0,
            bg="white",
            fg=self.colors["text_primary"],
            insertbackground=self.colors["text_primary"]
        )
        self.input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=8)
        self.input.bind("<Return>", self._submit)
        send_btn = tk.Button(
            input_frame,
            text="➤",
            command=self._submit,
            bg=self.colors["accent"],
            fg="white",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            activebackground=self.colors["accent_hover"],
            activeforeground="white",
            cursor="hand2",
            padx=15
        )
        send_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        self._show_intro()
    def _show_intro(self):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, "\n\n")
        self.output.insert(tk.END, "  How can I help you today?\n", "user_label")
        self.output.tag_config("intro", font=("Segoe UI", 24, "bold"), justify="center", foreground="#DDDDDD")
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "\n\n\nHow can I help you today?", "intro")
        self.output.configure(state=tk.DISABLED)
    def _submit(self, event=None):
        text = self.input.get().strip()
        if not text:
            return
        if "How can I help you today?" in self.output.get("1.0", "1.end"):
            self.output.configure(state=tk.NORMAL)
            self.output.delete("1.0", tk.END)
            self.output.configure(state=tk.DISABLED)
        self.input.delete(0, tk.END)
        self._add("You", text, is_user=True)
        self.update_idletasks()
        result = self.supervisor.handle_user_input(
            user_input=text,
            mode=self.get_mode()
        )
        self._add("Assistant", result.get("response", ""), is_user=False)
    def _add(self, sender, message, is_user=False):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, "\n", "divider")
        if is_user:
            self.output.insert(tk.END, f"👤 {sender}\n", "user_label")
            self.output.insert(tk.END, f"{message}\n", "user_msg")
        else:
            self.output.insert(tk.END, f"🤖 {sender}\n", "agent_label")
            self.output.insert(tk.END, f"{message}\n", "agent_msg")
        self.output.configure(state=tk.DISABLED)
        self.output.see(tk.END)
    def on_show(self):
        self.input.focus_set()