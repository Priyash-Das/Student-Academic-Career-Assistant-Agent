import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, simpledialog
from ui.workspace.base import BaseWorkspace
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'resume_builder'))
from resume_builder.core.resume_agent import ResumeAgent
from resume_builder.core.resume_schema import ResumeSchema, Header, Skills
from resume_builder.core.resume_validator import ResumeValidator
from resume_builder.renderer.docx_renderer import DocxRenderer
class ResumeWorkspace(BaseWorkspace):
    def __init__(self, parent, supervisor, colors):
        super().__init__(parent, supervisor)
        self.colors = colors
        self.current_resume = None
        self.validator = ResumeValidator()
        self.renderer = DocxRenderer()
        self._build_ui()
    def _build_ui(self):
        self.config(bg=self.colors["bg_main"])
        header_frame = tk.Frame(self, bg=self.colors["bg_main"])
        header_frame.pack(fill=tk.X, padx=40, pady=(18, 10))
        tk.Label(
            header_frame,
            text="AI Resume Builder",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["bg_main"],
            fg=self.colors["text_primary"]
        ).pack(anchor="w")
        tk.Label(
            header_frame,
            text="Generate a professional resume from a description, edit sections, and export to DOCX.",
            font=("Segoe UI", 11),
            bg=self.colors["bg_main"],
            fg=self.colors["text_secondary"]
        ).pack(anchor="w", pady=(5, 0))
        paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=self.colors["bg_main"], sashwidth=4)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=40, pady=10)
        left_frame = tk.Frame(paned_window, bg=self.colors["bg_main"])
        paned_window.add(left_frame, minsize=400, width=450)
        input_card = self._create_card(left_frame)
        input_card.pack(fill=tk.X, pady=(0, 20))
        tk.Label(
            input_card, 
            text="1. Profile Description", 
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg=self.colors["text_primary"]
        ).pack(anchor="w", padx=15, pady=(15, 5))
        self.prompt_box = scrolledtext.ScrolledText(
            input_card,
            height=8,
            font=("Segoe UI", 10),
            wrap="word",
            bg="white",
            bd=1,
            relief="solid"
        )
        self.prompt_box.config(highlightthickness=0, borderwidth=1)
        self.prompt_box.pack(fill=tk.X, padx=15, pady=(0, 15))
        self.placeholder = "Example: I am a Software Engineer with 5 years experience in Python..."
        self.prompt_box.insert("1.0", self.placeholder)
        self.prompt_box.config(fg="#999999")
        self.prompt_box.bind("<FocusIn>", self._on_focus_in)
        self.prompt_box.bind("<FocusOut>", self._on_focus_out)
        btn_row = tk.Frame(input_card, bg="white")
        btn_row.pack(fill=tk.X, padx=15, pady=(0, 15))
        self.generate_btn = tk.Button(
            btn_row,
            text="🚀 Generate",
            command=self._on_generate,
            font=("Segoe UI", 10, "bold"),
            bg=self.colors["accent"],
            fg="white",
            bd=0,
            padx=15, pady=8,
            cursor="hand2"
        )
        self.generate_btn.pack(side="left", fill=tk.X, expand=True, padx=(0, 5))
        self.demo_btn = tk.Button(
            btn_row,
            text="Load Demo",
            command=self._load_demo,
            font=("Segoe UI", 10),
            bg="#E0E0E0",
            fg="black",
            bd=0,
            padx=15, pady=8,
            cursor="hand2"
        )
        self.demo_btn.pack(side="right", fill=tk.X, expand=True, padx=(5, 0))
        edit_card = self._create_card(left_frame)
        edit_card.pack(fill=tk.X, pady=(0, 20))
        tk.Label(
            edit_card, 
            text="2. Edit Sections", 
            font=("Segoe UI", 11, "bold"),
            bg="white",
            fg=self.colors["text_primary"]
        ).pack(anchor="w", padx=15, pady=(15, 10))
        self.edit_btn_frame = tk.Frame(edit_card, bg="white")
        self.edit_btn_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        sections = [
            ("Personal Info", self._edit_header),
            ("Summary", self._edit_summary),
            ("Experience", self._edit_experience),
            ("Projects", self._edit_projects),
            ("Education", self._edit_education),
            ("Skills", self._edit_skills),
            ("Certifications", self._edit_certifications),
            ("Hobbies", self._edit_hobbies),
            ("Career Goal", self._edit_career_goal)
        ]
        for i, (label, cmd) in enumerate(sections):
            btn = tk.Button(
                self.edit_btn_frame,
                text=f"✏️ {label}",
                command=cmd,
                font=("Segoe UI", 9),
                bg="#F5F5F5",
                bd=0,
                cursor="hand2",
                state="disabled"
            )
            btn.grid(row=i//2, column=i%2, sticky="ew", padx=2, pady=2)
            setattr(self, f"btn_edit_{i}", btn)
        self.edit_btn_frame.columnconfigure(0, weight=1)
        self.edit_btn_frame.columnconfigure(1, weight=1)
        export_card = self._create_card(left_frame)
        export_card.pack(fill=tk.X)
        self.export_btn = tk.Button(
            export_card,
            text="💾 Download as .DOCX",
            command=self._on_export,
            font=("Segoe UI", 10, "bold"),
            bg="#2196F3",
            fg="white",
            bd=0,
            padx=15, pady=10,
            cursor="hand2",
            state="disabled"
        )
        self.export_btn.pack(fill=tk.X, padx=15, pady=15)
        right_frame = tk.Frame(paned_window, bg="#E5E5E5", bd=1)
        paned_window.add(right_frame, stretch="always")
        preview_container = tk.Frame(right_frame, bg="#E5E5E5", padx=20, pady=20)
        preview_container.pack(fill=tk.BOTH, expand=True)
        self.preview_text = tk.Text(
            preview_container,
            font=("Times New Roman", 12),
            wrap="word",
            bg="white",
            fg="black",
            bd=0,
            padx=40,
            pady=40,
            state="disabled"
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True)
        self._configure_preview_tags()
    def _create_card(self, parent):
        frame = tk.Frame(parent, bg="white", bd=1, relief="solid")
        try: frame.config(highlightbackground="#E5E5E5", highlightthickness=1, bd=0)
        except: pass
        return frame
    def _configure_preview_tags(self):
        t = self.preview_text
        t.tag_config("NAME", font=("Arial", 22, "bold"), justify="center", spacing3=10)
        t.tag_config("CONTACT", font=("Arial", 10), justify="center", foreground="#666666", spacing3=20)
        t.tag_config("SECTION", font=("Arial", 12, "bold", "underline"), spacing1=15, spacing3=5)
        t.tag_config("BOLD", font=("Times New Roman", 12, "bold"))
        t.tag_config("DATE", foreground="#666666")
        t.tag_config("BULLET", lmargin1=20, lmargin2=35, spacing1=3)
        t.tag_config("NORMAL", font=("Times New Roman", 12))
    def _on_focus_in(self, event):
        if self.prompt_box.get("1.0", "end-1c") == self.placeholder:
            self.prompt_box.delete("1.0", "end")
            self.prompt_box.config(fg="black")
    def _on_focus_out(self, event):
        if not self.prompt_box.get("1.0", "end-1c").strip():
            self.prompt_box.insert("1.0", self.placeholder)
            self.prompt_box.config(fg="#999999")
    def _on_generate(self):
        prompt = self.prompt_box.get("1.0", "end-1c").strip()
        if not prompt or prompt == self.placeholder:
            messagebox.showwarning("Input Required", "Please describe your profile.")
            return
        self.generate_btn.config(text="Generating...", state="disabled")
        self.update_idletasks()
        try:
            generated = ResumeAgent.generate_from_prompt(prompt)
            self.current_resume = self.validator.validate(generated)
            self._update_preview()
            self._enable_controls()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.generate_btn.config(text="🚀 Generate", state="normal")
    def _load_demo(self):
        try:
            demo = ResumeAgent.generate_demo_resume()
            self.current_resume = demo
            self._update_preview()
            self._enable_controls()
            self.prompt_box.delete("1.0", tk.END)
            self.prompt_box.config(fg="black")
            self.prompt_box.insert("1.0", "✓ Demo loaded. You can now edit sections using the buttons below.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def _on_export(self):
        if not self.current_resume: return
        path = filedialog.asksaveasfilename(
            defaultextension=".docx", 
            filetypes=[("Word Document", "*.docx")]
        )
        if path:
            try:
                self.renderer.render(self.current_resume, path)
                messagebox.showinfo("Success", "Resume exported successfully!")
            except Exception as e:
                messagebox.showerror("Export Error", str(e))
    def _enable_controls(self):
        self.export_btn.config(state="normal")
        for i in range(9):
            btn = getattr(self, f"btn_edit_{i}", None)
            if btn: btn.config(state="normal")
    def _update_preview(self):
        r = self.current_resume
        if not r: return
        t = self.preview_text
        t.config(state="normal")
        t.delete("1.0", tk.END)
        t.insert(tk.END, f"{r.header.name.upper()}\n", "NAME")
        parts = [p for p in [r.header.email, r.header.phone, r.header.address, r.header.linkedin] if p]
        t.insert(tk.END, " | ".join(parts) + "\n\n", "CONTACT")
        if r.summary:
            t.insert(tk.END, "PROFESSIONAL SUMMARY\n", "SECTION")
            t.insert(tk.END, f"{r.summary}\n\n", "NORMAL")
        if r.experience:
            t.insert(tk.END, "EXPERIENCE\n", "SECTION")
            for exp in r.experience:
                t.insert(tk.END, f"{exp.role}", "BOLD")
                t.insert(tk.END, f" | {exp.company}", "NORMAL")
                if exp.dates:
                    t.insert(tk.END, f" ({exp.dates})", "DATE")
                t.insert(tk.END, "\n", "NORMAL")
                for b in exp.bullets:
                    t.insert(tk.END, f"• {b}\n", "BULLET")
                t.insert(tk.END, "\n")
        if r.education:
            t.insert(tk.END, "EDUCATION\n", "SECTION")
            for edu in r.education:
                t.insert(tk.END, f"{edu.degree}", "BOLD")
                t.insert(tk.END, f", {edu.institution}", "NORMAL")
                if edu.year:
                    t.insert(tk.END, f" ({edu.year})", "DATE")
                t.insert(tk.END, "\n", "NORMAL")
                for d in edu.details:
                    t.insert(tk.END, f"• {d}\n", "BULLET")
                t.insert(tk.END, "\n")
        s = r.skills
        if any([s.programming_languages, s.frameworks_libraries, s.tools_technologies]):
            t.insert(tk.END, "SKILLS\n", "SECTION")
            if s.programming_languages:
                t.insert(tk.END, "Languages: ", "BOLD")
                t.insert(tk.END, ", ".join(s.programming_languages) + "\n", "NORMAL")
            if s.frameworks_libraries:
                t.insert(tk.END, "Frameworks: ", "BOLD")
                t.insert(tk.END, ", ".join(s.frameworks_libraries) + "\n", "NORMAL")
            if s.tools_technologies:
                t.insert(tk.END, "Tools: ", "BOLD")
                t.insert(tk.END, ", ".join(s.tools_technologies) + "\n", "NORMAL")
            t.insert(tk.END, "\n")
        if r.hobbies:
            t.insert(tk.END, "HOBBIES & INTERESTS\n", "SECTION")
            t.insert(tk.END, ", ".join(r.hobbies) + "\n", "NORMAL")
        if r.career_goal:
            t.insert(tk.END, "\nCAREER GOAL\n", "SECTION")
            t.insert(tk.END, f"{r.career_goal}\n", "NORMAL")
        t.config(state="disabled")
    def _edit_header(self):
        if not self.current_resume: return
        dialog = EditHeaderDialog(self, self.current_resume.header)
        self.wait_window(dialog)
        self._update_preview()
    def _edit_summary(self):
        if not self.current_resume: return
        new_sum = simpledialog.askstring("Edit Summary", "Professional Summary:", initialvalue=self.current_resume.summary, parent=self)
        if new_sum is not None:
            self.current_resume.summary = new_sum
            self._update_preview()
    def _edit_career_goal(self):
        if not self.current_resume: return
        new_goal = simpledialog.askstring("Edit Goal", "Career Goal:", initialvalue=self.current_resume.career_goal, parent=self)
        if new_goal is not None:
            self.current_resume.career_goal = new_goal
            self._update_preview()
    def _edit_experience(self):
        messagebox.showinfo("Info", "To edit Experience, please modify the prompt on the left and Regenerate.\n(Complex list editing not supported in this simplified view)")
    def _edit_projects(self):
        messagebox.showinfo("Info", "To edit Projects, please modify the prompt on the left and Regenerate.")
    def _edit_education(self):
        messagebox.showinfo("Info", "To edit Education, please modify the prompt on the left and Regenerate.")
    def _edit_skills(self):
        if not self.current_resume: return
        s = self.current_resume.skills
        curr = ", ".join(s.tools_technologies)
        new_val = simpledialog.askstring("Edit Skills", "Add/Edit Skills (comma separated):", initialvalue=curr, parent=self)
        if new_val is not None:
            s.tools_technologies = [x.strip() for x in new_val.split(",") if x.strip()]
            self._update_preview()
    def _edit_certifications(self):
        messagebox.showinfo("Info", "To edit Certifications, please modify the prompt.")
    def _edit_hobbies(self):
        if not self.current_resume: return
        curr = ", ".join(self.current_resume.hobbies)
        new_val = simpledialog.askstring("Edit Hobbies", "Hobbies (comma separated):", initialvalue=curr, parent=self)
        if new_val is not None:
            self.current_resume.hobbies = [x.strip() for x in new_val.split(",") if x.strip()]
            self._update_preview()
class EditHeaderDialog(tk.Toplevel):
    def __init__(self, parent, header):
        super().__init__(parent)
        self.title("Edit Personal Info")
        self.geometry("400x350")
        self.header = header
        self.grab_set()
        self.entries = {}
        fields = [
            ("Name", header.name), ("Email", header.email), 
            ("Phone", header.phone), ("Address", header.address), 
            ("LinkedIn", header.linkedin)
        ]
        for i, (label, val) in enumerate(fields):
            tk.Label(self, text=label, font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(10, 0))
            e = tk.Entry(self, font=("Segoe UI", 10))
            e.insert(0, val)
            e.pack(fill="x", padx=20, pady=(0, 5))
            self.entries[label] = e
        tk.Button(self, text="Save", command=self.save, bg="#27ae60", fg="white").pack(pady=20)
    def save(self):
        self.header.name = self.entries["Name"].get()
        self.header.email = self.entries["Email"].get()
        self.header.phone = self.entries["Phone"].get()
        self.header.address = self.entries["Address"].get()
        self.header.linkedin = self.entries["LinkedIn"].get()
        self.destroy()