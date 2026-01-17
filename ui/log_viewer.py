import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import json
import os
from pathlib import Path
from datetime import datetime
from utils.log_manager import LogManager
from utils.logger import LogLevel, LogCategory
class LogViewerWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Centralized Log Viewer")
        self.window.geometry("1200x800")
        self.window.configure(bg="white")
        self.current_logs = []
        self.filter_level = "ALL"
        self.filter_agent = "ALL"
        self._setup_ui()
        self._load_logs()
    def _setup_ui(self):
        control_frame = ttk.Frame(self.window)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        ttk.Label(control_frame, text="Filter by Level:").pack(side=tk.LEFT, padx=5)
        self.level_combo = ttk.Combobox(control_frame, 
                                       values=["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "AUDIT", "AGENT"],
                                       state="readonly")
        self.level_combo.set("ALL")
        self.level_combo.pack(side=tk.LEFT, padx=5)
        self.level_combo.bind("<<ComboboxSelected>>", self._apply_filters)
        ttk.Label(control_frame, text="Filter by Agent:").pack(side=tk.LEFT, padx=5)
        self.agent_combo = ttk.Combobox(control_frame,
                                       values=["ALL", "RESUME_AGENT", "STUDY_BUDDY", "VOICE_NOTES", 
                                               "WEBSITE_AGENT", "CHAT_AGENT", "UI", "SYSTEM"],
                                       state="readonly")
        self.agent_combo.set("ALL")
        self.agent_combo.pack(side=tk.LEFT, padx=5)
        self.agent_combo.bind("<<ComboboxSelected>>", self._apply_filters)
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="🔄 Refresh", 
                  command=self._load_logs).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="📥 Export JSON", 
                  command=self._export_logs).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="📋 Copy All", 
                  command=self._copy_logs).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="🗑️ Clear Display", 
                  command=self._clear_display).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="📄 View Raw File", 
                  command=self._view_raw_file).pack(side=tk.LEFT, padx=2)
        ttk.Label(control_frame, text="Search:").pack(side=tk.LEFT, padx=(20, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<KeyRelease>", self._search_logs)
        stats_frame = ttk.Frame(self.window)
        stats_frame.pack(fill=tk.X, padx=10, pady=(0, 5))
        self.stats_label = ttk.Label(stats_frame, text="Total logs: 0 | Showing: 0")
        self.stats_label.pack(side=tk.LEFT)
        self.current_file_label = ttk.Label(stats_frame, text="", foreground="gray")
        self.current_file_label.pack(side=tk.RIGHT)
        display_frame = ttk.Frame(self.window)
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.tree = ttk.Treeview(display_frame, 
                                columns=("Time", "Level", "Agent", "Category", "Message"),
                                show="headings",
                                selectmode="extended")
        self.tree.heading("Time", text="Timestamp", command=lambda: self._sort_column("Time", False))
        self.tree.heading("Level", text="Level", command=lambda: self._sort_column("Level", False))
        self.tree.heading("Agent", text="Agent", command=lambda: self._sort_column("Agent", False))
        self.tree.heading("Category", text="Category", command=lambda: self._sort_column("Category", False))
        self.tree.heading("Message", text="Message", command=lambda: self._sort_column("Message", False))
        self.tree.column("Time", width=150)
        self.tree.column("Level", width=80)
        self.tree.column("Agent", width=120)
        self.tree.column("Category", width=100)
        self.tree.column("Message", width=500)
        yscrollbar = ttk.Scrollbar(display_frame, orient="vertical", command=self.tree.yview)
        xscrollbar = ttk.Scrollbar(display_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscrollbar.set, xscrollcommand=xscrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        yscrollbar.grid(row=0, column=1, sticky="ns")
        xscrollbar.grid(row=1, column=0, sticky="ew")
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)
        details_frame = ttk.LabelFrame(self.window, text="Log Details", padding=10)
        details_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.details_text = scrolledtext.ScrolledText(details_frame, height=8, wrap=tk.WORD)
        self.details_text.pack(fill=tk.BOTH, expand=True)
        self.details_text.configure(state="disabled")
        self.tree.bind("<<TreeviewSelect>>", self._show_details)
        LogManager.ui_event("window_opened", "LogViewer", "view_logs")
    def _load_logs(self):
        try:
            self.current_logs = LogManager.get_recent_logs(500) 
            self._update_display()
            total = len(self.current_logs)
            showing = len(self.tree.get_children())
            self.stats_label.config(text=f"Total logs: {total} | Showing: {showing}")
            log_file = LogManager.get_current_log_file()
            self.current_file_label.config(text=f"Log file: {Path(log_file).name}")
            LogManager.ui_event("logs_refreshed", "LogViewer", 
                              details={"total_logs": total})
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load logs: {str(e)}")
            LogManager.error(f"Failed to load logs in viewer: {str(e)}", agent="UI")
    def _update_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        filtered_logs = self._filter_logs(self.current_logs)
        for log in filtered_logs:
            level = log.get("level", "INFO")
            tags = ()
            if level == "ERROR" or level == "CRITICAL":
                tags = ("error",)
            elif level == "WARNING":
                tags = ("warning",)
            elif level == "DEBUG":
                tags = ("debug",)
            elif level == "AUDIT":
                tags = ("audit",)
            timestamp = log.get("timestamp", "")
            if "T" in timestamp:
                timestamp = timestamp.replace("T", " ").split(".")[0]
            self.tree.insert("", "end", 
                           values=(timestamp,
                                   level,
                                   log.get("module", "UNKNOWN"),
                                   log.get("category", "SYSTEM"),
                                   log.get("message", "")[:100]),
                           tags=tags)
        self.tree.tag_configure("error", background="#ffe6e6")
        self.tree.tag_configure("warning", background="#fff3cd")
        self.tree.tag_configure("debug", foreground="#6c757d")
        self.tree.tag_configure("audit", background="#e6f7ff")
    def _filter_logs(self, logs):
        filtered = logs
        if self.filter_level != "ALL":
            filtered = [log for log in filtered if log.get("level") == self.filter_level]
        if self.filter_agent != "ALL":
            filtered = [log for log in filtered if log.get("module") == self.filter_agent]
        search_text = self.search_var.get().lower()
        if search_text:
            filtered = [log for log in filtered 
                       if search_text in str(log).lower() or 
                       search_text in log.get("message", "").lower()]
        return filtered
    def _apply_filters(self, event=None):
        self.filter_level = self.level_combo.get()
        self.filter_agent = self.agent_combo.get()
        self._update_display()
        total = len(self.current_logs)
        showing = len(self.tree.get_children())
        self.stats_label.config(text=f"Total logs: {total} | Showing: {showing}")
        LogManager.ui_event("logs_filtered", "LogViewer",
                          details={"level_filter": self.filter_level,
                                   "agent_filter": self.filter_agent})
    def _search_logs(self, event=None):
        self._apply_filters()
    def _sort_column(self, col, reverse):
        data = [(self.tree.set(child, col), child) for child in self.tree.get_children()]
        data.sort(reverse=reverse)
        for index, (_, child) in enumerate(data):
            self.tree.move(child, "", index)
        self.tree.heading(col, command=lambda: self._sort_column(col, not reverse))
    def _show_details(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        item = self.tree.item(selection[0])
        values = item["values"]
        timestamp = values[0].replace(" ", "T")  
        for log in self.current_logs:
            if timestamp in str(log.get("timestamp", "")):
                self.details_text.configure(state="normal")
                self.details_text.delete(1.0, tk.END)
                try:
                    formatted = json.dumps(log, indent=2, default=str)
                    self.details_text.insert(tk.END, formatted)
                except:
                    self.details_text.insert(tk.END, str(log))
                
                self.details_text.configure(state="disabled")
                break
    def _export_logs(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"app_logs_export_{timestamp}.json"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialfile=default_name
            )
            if file_path:
                export_path = LogManager.export_logs(file_path)
                messagebox.showinfo("Success", f"Logs exported to:\n{export_path}")
                LogManager.audit("logs_exported",
                               details={"export_path": export_path})
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export logs: {str(e)}")
            LogManager.error(f"Failed to export logs: {str(e)}", agent="UI")
    def _copy_logs(self):
        try:
            logs_text = []
            for child in self.tree.get_children():
                values = self.tree.item(child)["values"]
                logs_text.append("\t".join(str(v) for v in values))
            if logs_text:
                self.window.clipboard_clear()
                self.window.clipboard_append("\n".join(logs_text))
                messagebox.showinfo("Success", "Logs copied to clipboard")
                LogManager.audit("logs_copied",
                               details={"log_count": len(logs_text)})
            else:
                messagebox.showwarning("Warning", "No logs to copy")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy logs: {str(e)}")
    def _clear_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.details_text.configure(state="normal")
        self.details_text.delete(1.0, tk.END)
        self.details_text.configure(state="disabled")
        self.stats_label.config(text="Total logs: 0 | Showing: 0")
        LogManager.ui_event("logs_cleared", "LogViewer")
    def _view_raw_file(self):
        try:
            log_file = LogManager.get_current_log_file()
            import platform
            import subprocess
            if platform.system() == "Windows":
                os.startfile(log_file)
            elif platform.system() == "Darwin":  
                subprocess.run(["open", log_file])
            else:  
                subprocess.run(["xdg-open", log_file])
            LogManager.audit("raw_log_file_opened",
                           details={"file_path": log_file})
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open log file: {str(e)}")
            LogManager.error(f"Failed to open raw log file: {str(e)}", agent="UI")
    def show(self):
        self.window.transient(self.parent)
        self.window.grab_set()
        self.window.focus_set()
        self.parent.wait_window(self.window)
class LogSidebarButton:
    def __init__(self, sidebar_frame, colors):
        self.sidebar_frame = sidebar_frame
        self.colors = colors
        self.button = tk.Button(
            sidebar_frame,
            text="📊 View Logs",
            font=("Segoe UI", 10),
            bg=colors["bg_sidebar"],
            fg=colors["text_primary"],
            relief="flat",
            cursor="hand2",
            command=self._open_log_viewer
        )
        self.button.pack(fill=tk.X, padx=10, pady=2)
        self.button.bind("<Enter>", lambda e: self.button.config(bg="#e0e0e0"))
        self.button.bind("<Leave>", lambda e: self.button.config(bg=colors["bg_sidebar"]))
    def _open_log_viewer(self):
        LogManager.ui_event("sidebar_button_clicked", "LogViewerButton", "view_logs")
        LogViewerWindow(self.sidebar_frame.winfo_toplevel())