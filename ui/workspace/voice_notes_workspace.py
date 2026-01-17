import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
from ui.workspace.base import BaseWorkspace
import os
class VoiceNotesWorkspace(BaseWorkspace):
    def __init__(self, parent, supervisor, colors):
        super().__init__(parent, supervisor, colors)
        self._build_ui()
    def _build_ui(self):
        header = tk.Frame(self, bg=self.colors["bg_main"])
        header.pack(fill=tk.X, padx=40, pady=(30, 10))
        tk.Label(
            header,
            text="Voice-to-Notes Generator",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["bg_main"],
            fg=self.colors["text_primary"]
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Upload audio lectures to generate structured notes.",
            font=("Segoe UI", 11),
            bg=self.colors["bg_main"],
            fg=self.colors["text_secondary"]
        ).pack(anchor="w", pady=(5, 0))
        controls = tk.Frame(self, bg=self.colors["bg_main"])
        controls.pack(fill=tk.X, padx=40, pady=10)
        tk.Button(
            controls,
            text="📎 Upload Audio",
            command=self._upload_audio,
            font=("Segoe UI", 10),
            bg=self.colors["accent"],
            fg="white",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2"
        ).pack(side=tk.LEFT)
        self.file_label = tk.Label(
            controls,
            text="No file uploaded",
            bg=self.colors["bg_main"],
            fg=self.colors["text_secondary"],
            font=("Segoe UI", 10, "italic"),
            padx=15
        )
        self.file_label.pack(side=tk.LEFT)
        action_frame = tk.Frame(self, bg=self.colors["bg_main"])
        action_frame.pack(fill=tk.X, padx=40, pady=10)
        self.generate_notes_btn = tk.Button(
            action_frame,
            text="Generate Notes",
            command=self._generate_notes,
            font=("Segoe UI", 10, "bold"),
            bg="#2196F3",
            fg="white",
            bd=0,
            padx=15,
            pady=8,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.generate_notes_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.export_btn = tk.Button(
            action_frame,
            text="Export DOCX",
            command=self._export_notes,
            font=("Segoe UI", 10),
            bg="#FF9800", 
            fg="white",
            bd=0,
            padx=15,
            pady=8,
            state=tk.DISABLED,
            cursor="hand2"
        )
        self.export_btn.pack(side=tk.LEFT)
        self.output = ScrolledText(
            self,
            state=tk.DISABLED,
            wrap=tk.WORD,
            font=("Segoe UI", 11),
            bg="#F7F7F8",
            bd=0,
            padx=20,
            pady=20,
            highlightthickness=0,
            height=12
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        qa_frame = tk.Frame(self, bg=self.colors["bg_main"])
        qa_frame.pack(fill=tk.X, padx=40, pady=20)
        tk.Label(qa_frame, text="Ask from Notes:", font=("Segoe UI", 10, "bold"), bg=self.colors["bg_main"]).pack(side=tk.LEFT)
        self.qa_input = tk.Entry(qa_frame, font=("Segoe UI", 11), bd=1, relief=tk.SOLID)
        self.qa_input.config(highlightbackground=self.colors["border"], highlightthickness=1, bd=0)
        self.qa_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, ipady=5)
        self.qa_input.bind("<Return>", lambda e: self._ask_question())
        self.qa_btn = tk.Button(
            qa_frame,
            text="Ask",
            command=self._ask_question,
            bg=self.colors["accent"],
            fg="white",
            bd=0,
            padx=15,
            pady=5,
            state=tk.DISABLED
        )
        self.qa_btn.pack(side=tk.LEFT)
    def _upload_audio(self):
        file_path = filedialog.askopenfilename(
            title="Select Audio File",
            filetypes=[("Audio Files", "*.wav *.mp3 *.m4a *.ogg *.flac"), ("All Files", "*.*")]
        )
        if not file_path: return
        try:
            result = self.supervisor.upload_audio(file_path)
            self.file_label.config(text=os.path.basename(file_path), fg=self.colors["accent"])
            self.generate_notes_btn.config(state=tk.NORMAL)
            self._add("System", f"Audio uploaded: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Upload Error", str(e))
    def _generate_notes(self):
        try:
            self._add("System", "Transcribing audio (this may take a moment)...")
            self.generate_notes_btn.config(state=tk.DISABLED, text="Processing...")
            self.update_idletasks()
            result = self.supervisor.handle_user_input("generate notes")
            if result.get("agent") == "VOICE_NOTES":
                notes = result.get("response", "")
                if notes and not notes.startswith("Voice-to-Notes error"):
                    self._add("Notes", notes)
                    self.export_btn.config(state=tk.NORMAL)
                    self.qa_input.config(state=tk.NORMAL)
                    self.qa_btn.config(state=tk.NORMAL)
                else:
                    self._add("Error", notes)
        except Exception as e:
            self._add("Error", str(e))
        finally:
            self.generate_notes_btn.config(state=tk.NORMAL, text="Generate Notes")
    def _export_notes(self):
        try:
            notes = self.supervisor.voice_notes_agent.get_notes()
        except Exception: notes = None
        if not notes: return
        file_path = filedialog.asksaveasfilename(defaultextension=".docx", filetypes=[("Word Document", "*.docx")])
        if not file_path: return
        try:
            from voice_to_notes_generator.utils.docx_exporter import export_notes_to_docx
            export_notes_to_docx(notes, file_path)
            messagebox.showinfo("Export Successful", f"Saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
    def _ask_question(self):
        question = self.qa_input.get().strip()
        if not question: return
        self._add("You", question)
        self.qa_input.delete(0, tk.END)
        try:
            result = self.supervisor.handle_user_input(question)
            if result.get("agent") == "VOICE_NOTES":
                self._add("Agent", result.get("response", ""))
            else:
                self._add("Error", "Failed to get answer.")
        except Exception as e:
            self._add("Error", str(e))
    def _add(self, sender, message):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, f"[{sender}]\n{message}\n\n")
        self.output.configure(state=tk.DISABLED)
        self.output.see(tk.END)