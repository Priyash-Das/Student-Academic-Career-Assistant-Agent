import tkinter as tk
class Sidebar(tk.Frame):
    def __init__(self, parent, on_select, colors):
        super().__init__(parent, width=260, bg=colors["bg_sidebar"])
        self.pack_propagate(False)
        self.on_select = on_select
        self.colors = colors
        self.buttons = {}
        title_frame = tk.Frame(self, bg=colors["bg_sidebar"], height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        tk.Label(
            title_frame,
            text="AI Assistant",
            font=("Segoe UI", 16, "bold"),
            bg=colors["bg_sidebar"],
            fg=colors["text_primary"]
        ).pack(side=tk.LEFT, padx=20, pady=25)
        self._create_nav_button("💬 Your Chat", "CHAT", primary=True)
        tk.Frame(self, height=1, bg="#E5E5E5").pack(fill=tk.X, padx=15, pady=15)
        tk.Label(
            self,
            text="TOOLS",
            font=("Segoe UI", 9, "bold"),
            bg=colors["bg_sidebar"],
            fg="#999999"
        ).pack(anchor="w", padx=20, pady=(10, 5))
        tools = [
            ("📚  Study Buddy", "STUDY_BUDDY"),
            ("🎤  Voice Notes", "VOICE_NOTES"),
            ("📄  Resume Builder", "RESUME"),
            ("🌐  Website Builder", "WEBSITE"),
        ]
        for label, key in tools:
            self._create_nav_button(label, key)
        tk.Frame(self, height=1, bg="#E5E5E5").pack(fill=tk.X, padx=15, pady=15)
        tk.Label(
            self,
            text="LOGS",
            font=("Segoe UI", 9, "bold"),
            bg=colors["bg_sidebar"],
            fg="#999999"
        ).pack(anchor="w", padx=20, pady=(10, 5))
        self._create_log_button()
        tk.Label(
            self,
            text="v1.0.0",
            font=("Segoe UI", 8),
            bg=colors["bg_sidebar"],
            fg="#CCCCCC"
        ).pack(side=tk.BOTTOM, pady=20)
    def _create_log_button(self):
        import tkinter as tk
        log_button = tk.Button(
            self,
            text="📊 View Logs",
            font=("Segoe UI", 10),
            bg=self.colors["bg_sidebar"],
            fg=self.colors["text_primary"],
            relief="flat",
            cursor="hand2",
            command=self._open_log_viewer
        )
        log_button.pack(fill=tk.X, padx=10, pady=2)
        log_button.bind("<Enter>", lambda e: log_button.config(bg="#e0e0e0"))
        log_button.bind("<Leave>", lambda e: log_button.config(bg=self.colors["bg_sidebar"]))
        self.buttons["LOGS"] = log_button
    def _open_log_viewer(self):
        try:
            from ui.log_viewer import LogViewerWindow
            root = self.winfo_toplevel()
            log_viewer = LogViewerWindow(root)
            from utils.log_manager import LogManager
            LogManager.ui_event("sidebar_button_clicked", "LogViewerButton", 
                              details={"action": "open_log_viewer"})
        except ImportError as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", 
                               f"Log viewer module not available:\n{str(e)}")
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", 
                               f"Failed to open log viewer:\n{str(e)}")
    def _create_nav_button(self, text, key, primary=False):
        container = tk.Frame(self, bg=self.colors["bg_sidebar"])
        container.pack(fill=tk.X, padx=10, pady=2)
        bg_color = self.colors["bg_sidebar"]
        fg_color = self.colors["text_primary"]
        font = ("Segoe UI", 10)
        if primary:
            bg_color = "white"
            font = ("Segoe UI", 10, "bold")
            border_frame = tk.Frame(container, bg="#DDDDDD", bd=1)
            border_frame.pack(fill=tk.BOTH, padx=0, pady=0)
            btn_parent = border_frame
        else:
            btn_parent = container
        btn = tk.Button(
            btn_parent,
            text=text,
            bg=bg_color,
            fg=fg_color,
            activebackground="#E0E0E0",
            activeforeground="black",
            font=font,
            bd=0,
            cursor="hand2",
            anchor="w",
            padx=15,
            pady=10,
            command=lambda k=key: self.on_select(k)
        )
        btn.pack(fill=tk.BOTH, expand=True)
        self.buttons[key] = btn
    def set_active(self, active_key):
        for key, btn in self.buttons.items():
            if key == active_key:
                btn.config(bg="#E0E0E0", font=("Segoe UI", 10, "bold"))
            else:
                is_chat = (key == "CHAT")
                bg = "white" if is_chat else self.colors["bg_sidebar"]
                font = ("Segoe UI", 10, "bold") if is_chat else ("Segoe UI", 10)
                btn.config(bg=bg, font=font)