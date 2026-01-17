import tkinter as tk
from tkinter import messagebox, scrolledtext
from ui.workspace.base import BaseWorkspace
from website_builder.core.prompt_processor import PromptProcessor
from website_builder.core.spec_inference import WebsiteSpecInference
from website_builder.core.generator import WebsiteGenerator
from website_builder.core.sanitizer import OutputSanitizer
from website_builder.core.validator import HTMLValidator
from website_builder.core.health_check import HealthCheck
from website_builder.core.llm_client import LLMClient
from website_builder.preview.live_preview import LivePreview
from website_builder.export.copy_manager import CopyManager
from website_builder.export.download_manager import DownloadManager
class WebsiteWorkspace(BaseWorkspace):
    def __init__(self, parent, supervisor, colors):
        super().__init__(parent, supervisor, colors)
        self.html_output = ""
        self.api_client = LLMClient()
        self._build_ui()
        if self.html_output:
            self.set_action_buttons(True)
    def _build_ui(self):
        header = tk.Frame(self, bg=self.colors["bg_main"])
        header.pack(fill=tk.X, padx=40, pady=(30, 20))
        tk.Label(
            header,
            text="AI Website Builder",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["bg_main"],
            fg=self.colors["text_primary"]
        ).pack(anchor="w")
        input_frame = tk.Frame(self, bg=self.colors["bg_main"])
        input_frame.pack(fill=tk.BOTH, padx=40, pady=10)
        tk.Label(input_frame, text="Describe your website:", font=("Segoe UI", 10, "bold"), bg=self.colors["bg_main"]).pack(anchor="w", pady=(0, 5))
        self.prompt_box = scrolledtext.ScrolledText(
            input_frame, height=6, font=("Segoe UI", 11), wrap="word",
            bg="white", bd=1, relief=tk.SOLID
        )
        self.prompt_box.pack(fill=tk.X)
        tk.Label(input_frame, text="Modifications (optional):", font=("Segoe UI", 10, "bold"), bg=self.colors["bg_main"]).pack(anchor="w", pady=(15, 5))
        self.mod_box = scrolledtext.ScrolledText(
            input_frame, height=3, font=("Segoe UI", 11), wrap="word",
            bg="white", bd=1, relief=tk.SOLID
        )
        self.mod_box.pack(fill=tk.X)
        btn_frame = tk.Frame(self, bg=self.colors["bg_main"])
        btn_frame.pack(fill=tk.X, padx=40, pady=20)
        self.generate_btn = tk.Button(
            btn_frame,
            text="🚀 Generate Website",
            command=self.generate,
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["accent"],
            fg="white",
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.generate_btn.pack(side=tk.LEFT)
        self.status = tk.Label(btn_frame, text="Ready", font=("Segoe UI", 10), bg=self.colors["bg_main"], fg="#999999", padx=15)
        self.status.pack(side=tk.LEFT)
        action_frame = tk.Frame(self, bg=self.colors["bg_main"])
        action_frame.pack(fill=tk.X, padx=40, pady=0)
        self.preview_btn = self._create_action_btn(action_frame, "👁 Live Preview", self.preview)
        self.copy_btn = self._create_action_btn(action_frame, "📋 Copy Code", self.copy)
        self.download_btn = self._create_action_btn(action_frame, "💾 Download", self.download)
    def _create_action_btn(self, parent, text, cmd):
        btn = tk.Button(
            parent,
            text=text,
            command=cmd,
            font=("Segoe UI", 10),
            bg="#E0E0E0",
            fg="black",
            bd=0,
            padx=15,
            pady=8,
            state=tk.DISABLED,
            cursor="hand2"
        )
        btn.pack(side=tk.LEFT, padx=(0, 10))
        return btn
    def set_action_buttons(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        for btn in [self.preview_btn, self.copy_btn, self.download_btn]:
            btn.config(state=state)
    def generate(self):
        self.status.config(text="Processing...", fg="#F59E0B")
        self.generate_btn.config(state=tk.DISABLED)
        self.update_idletasks()
        try:
            prompt_text = self.prompt_box.get("1.0", tk.END).strip()
            mod_text = self.mod_box.get("1.0", tk.END).strip()
            if len(prompt_text) < 5:
                raise ValueError("Prompt too short.")
            processor = PromptProcessor(prompt_text, mod_text)
            spec = WebsiteSpecInference.infer(processor.merge())
            generator = WebsiteGenerator(self.api_client)
            result = generator.generate(spec)
            clean_html = OutputSanitizer.sanitize(result["html"])
            if HTMLValidator.is_valid(clean_html) and HealthCheck.run(clean_html):
                self.html_output = clean_html
                self.set_action_buttons(True)
                self.status.config(text="Completed", fg=self.colors["accent"])
                messagebox.showinfo("Success", "Website generated successfully!")
            else:
                raise ValueError("Validation failed.")
        except Exception as e:
            self.status.config(text="Error", fg="red")
            messagebox.showerror("Error", str(e))
        finally:
            self.generate_btn.config(state=tk.NORMAL)
    def preview(self):
        if self.html_output: LivePreview.open(self.html_output)
    def copy(self):
        if self.html_output: CopyManager.copy(self.html_output)
    def download(self):
        if self.html_output: DownloadManager.download(self.html_output)