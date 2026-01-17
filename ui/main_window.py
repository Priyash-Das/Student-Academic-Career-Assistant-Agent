import tkinter as tk
from tkinter import ttk
from ui.header import Header
from ui.sidebar import Sidebar
from ui.status_bar import StatusBar
from ui.workspace.chat_workspace import ChatWorkspace
from ui.workspace.study_buddy_workspace import StudyBuddyWorkspace
from ui.workspace.voice_notes_workspace import VoiceNotesWorkspace
from ui.workspace.resume_workspace import ResumeWorkspace
from ui.workspace.website_workspace import WebsiteWorkspace
class MainWindow:
    def __init__(self, root, supervisor):
        self.root = root
        self.supervisor = supervisor
        self.mode = "FAST"
        self.colors = {
            "bg_main": "#FFFFFF",
            "bg_sidebar": "#F7F7F8",
            "border": "#E5E5E5",
            "text_primary": "#202123",
            "text_secondary": "#6E6E80",
            "accent": "#10A37F",  
            "accent_hover": "#1A7F64"
        }
        root.title("Student Academic & Career Assistant")
        root.geometry("1280x850")
        root.configure(bg=self.colors["bg_main"])
        self._configure_styles()
        self.sidebar = Sidebar(root, self._switch_workspace, self.colors)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        content_area = tk.Frame(root, bg=self.colors["bg_main"])
        content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.header = Header(content_area, self._set_mode, self.colors)
        self.header.pack(side=tk.TOP, fill=tk.X)
        self.workspace_container = tk.Frame(content_area, bg=self.colors["bg_main"])
        self.workspace_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.status = StatusBar(content_area, self.colors)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        self.workspaces = {
            "CHAT": ChatWorkspace(self.workspace_container, supervisor, lambda: self.mode, self.colors),
            "STUDY_BUDDY": StudyBuddyWorkspace(self.workspace_container, supervisor, self.colors),
            "VOICE_NOTES": VoiceNotesWorkspace(self.workspace_container, supervisor, self.colors),
            "RESUME": ResumeWorkspace(self.workspace_container, supervisor, self.colors),
            "WEBSITE": WebsiteWorkspace(self.workspace_container, supervisor, self.colors),
        }
        self.active = None
        self._switch_workspace("CHAT")
    def _configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.colors["bg_main"])
        style.configure("TLabel", background=self.colors["bg_main"], foreground=self.colors["text_primary"], font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"), foreground=self.colors["text_primary"], background=self.colors["bg_main"])
        style.configure("TButton",
                        font=("Segoe UI", 10),
                        borderwidth=0,
                        focuscolor=self.colors["bg_main"],
                        background="#F0F0F0",
                        foreground=self.colors["text_primary"],
                        padding=6)
        style.map("TButton",
                  background=[("active", "#E0E0E0")],
                  foreground=[("active", "black")])
        style.configure("Accent.TButton",
                        background=self.colors["accent"],
                        foreground="white",
                        font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton",
                  background=[("active", self.colors["accent_hover"])])
        style.configure("TRadiobutton", background=self.colors["bg_main"], font=("Segoe UI", 10))
    def _set_mode(self, mode):
        self.mode = mode
        self.status.set(f"Mode switched to: {mode}")
    def _switch_workspace(self, key):
        if self.active:
            self.active.pack_forget()
            self.active.on_hide()
        if key not in self.workspaces:
            self.status.set(f"{key} UI not implemented yet")
            return
        self.supervisor.set_active_tool(key)
        self.sidebar.set_active(key)
        self.active = self.workspaces[key]
        self.active.pack(fill=tk.BOTH, expand=True)
        self.active.on_show()
        self.status.set(f"Active tool: {key}")
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
        button = tk.Button(
            container,
            text=text,
            font=font,
            bg=bg_color,
            fg=fg_color,
            relief="flat",
            anchor="w",
            cursor="hand2",
            command=lambda: self.on_select(key)
        )
        if primary:
            button.pack(fill=tk.BOTH, padx=10, pady=10)
            button.bind("<Enter>", lambda e: button.config(bg="#f0f0f0"))
            button.bind("<Leave>", lambda e: button.config(bg="white"))
        else:
            button.pack(fill=tk.X, padx=10, pady=6)
            button.bind("<Enter>", lambda e: button.config(bg="#e0e0e0"))
            button.bind("<Leave>", lambda e: button.config(bg=self.colors["bg_sidebar"]))
        self.buttons[key] = button
    def _create_log_button(self):
        container = tk.Frame(self, bg=self.colors["bg_sidebar"])
        container.pack(fill=tk.X, padx=10, pady=2)
        log_button = tk.Button(
            container,
            text="📊 View Logs",
            font=("Segoe UI", 10),
            bg=self.colors["bg_sidebar"],
            fg=self.colors["text_primary"],
            relief="flat",
            anchor="w",
            cursor="hand2",
            command=self._open_log_viewer
        )
        log_button.pack(fill=tk.X, padx=10, pady=6)
        log_button.bind("<Enter>", lambda e: log_button.config(bg="#e0e0e0"))
        log_button.bind("<Leave>", lambda e: log_button.config(bg=self.colors["bg_sidebar"]))
    def _open_log_viewer(self):
        try:
            from ui.log_viewer import LogViewerWindow
            from utils.log_manager import LogManager
            root = self.winfo_toplevel()
            log_viewer = LogViewerWindow(root)
            LogManager.ui_event("sidebar_button_clicked", "LogViewerButton", 
                              user_action="open_log_viewer")
        except ImportError as e:
            import tkinter.messagebox as messagebox
            messagebox.showinfo("Log Viewer", 
                              "Log viewer feature is being set up.\n\n" +
                              "Logs are being recorded and will be available soon.")
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("Error", f"Failed to open log viewer:\n{str(e)}")
    def set_active(self, key):
        for btn_key, button in self.buttons.items():
            if btn_key == key:
                button.config(bg="#e0e0e0", fg=self.colors["accent"])
            else:
                button.config(bg=self.colors["bg_sidebar"], fg=self.colors["text_primary"])