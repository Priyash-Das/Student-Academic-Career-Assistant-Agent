import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
class ChatArea(tk.Frame):
    def __init__(
        self,
        parent,
        on_submit,
        on_file_upload,
        on_audio_upload,
        on_copy_website,
        on_download_website,
        on_preview_website,
        on_new_session,
    ):
        super().__init__(parent)
        self.on_submit = on_submit
        self.on_file_upload = on_file_upload
        self.on_audio_upload = on_audio_upload
        self.on_copy_website = on_copy_website
        self.on_download_website = on_download_website
        self.on_preview_website = on_preview_website
        self.on_new_session = on_new_session
        self.output = ScrolledText(
            self,
            state=tk.DISABLED,
            wrap=tk.WORD,
            font=("Arial", 11)
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        controls = tk.Frame(self)
        controls.pack(fill=tk.X, padx=10, pady=(0, 10))
        tk.Button(
            controls, text="Upload PDF",
            command=self._upload_pdf
        ).pack(side=tk.LEFT)
        tk.Button(
            controls, text="Upload Audio",
            command=self._upload_audio
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            controls, text="Copy Website",
            command=self.on_copy_website
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            controls, text="Download Website",
            command=self._download_website
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            controls, text="Live Preview",
            command=self.on_preview_website
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            controls,
            text="New Session",
            command=self.on_new_session
        ).pack(side=tk.LEFT, padx=5)
        self.input = tk.Entry(controls, font=("Arial", 11))
        self.input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.input.bind("<Return>", self._submit)
    def _submit(self, event=None):
        text = self.input.get()
        self.input.delete(0, tk.END)
        self.on_submit(text)
    def _upload_pdf(self):
        path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")]
        )
        if path:
            self.on_file_upload(path)
    def _upload_audio(self):
        path = filedialog.askopenfilename(
            filetypes=[("Audio Files", "*.wav *.mp3 *.m4a")]
        )
        if path:
            self.on_audio_upload(path)
    def _download_website(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html")]
        )
        if path:
            self.on_download_website(path)
    def add_message(self, sender: str, message: str):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, f"{sender}:\n{message}\n\n")
        self.output.configure(state=tk.DISABLED)
        self.output.yview(tk.END)