import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import json
import re
from ui.workspace.base import BaseWorkspace
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
try:
    from study_buddy.pipelines.quiz_generator import generate_quiz
    from study_buddy.core.quiz_state import QuizState
    from study_buddy.core.context_builder import build_study_context
except ImportError:
    print("Warning: Study Buddy backend imports failed. Using mock data.")
    generate_quiz = None 
    QuizState = None
class QuestionFrame(tk.Frame):
    def __init__(self, parent, question_data, on_answer, colors):
        super().__init__(parent, bg="white", bd=1, relief="solid")
        try: self.config(highlightbackground="#E5E5E5", highlightthickness=1, bd=0)
        except: pass
        self.question_data = question_data
        self.on_answer = on_answer
        self.colors = colors
        self.selected_var = tk.StringVar()
        self.answered = False
        self.buttons = {}
        self._build_ui()
    def _build_ui(self):
        lbl_q = tk.Label(
            self, 
            text=self.question_data["question"],
            font=("Segoe UI", 12, "bold"),
            bg="white", 
            fg="#333333",
            wraplength=500, 
            justify="left"
        )
        lbl_q.pack(anchor="w", padx=20, pady=(20, 15))
        options_frame = tk.Frame(self, bg="white")
        options_frame.pack(fill="x", padx=20, pady=(0, 20))
        style = ttk.Style()
        style.configure("Quiz.TRadiobutton", background="white", font=("Segoe UI", 11))
        options = self.question_data["options"]
        iterable = options.items() if isinstance(options, dict) else enumerate(options)
        for key, text in iterable:
            val_key = str(key)
            disp_text = str(text)
            frame = tk.Frame(options_frame, bg="white", pady=5)
            frame.pack(fill="x")
            rb = ttk.Radiobutton(
                frame,
                text=disp_text,
                variable=self.selected_var,
                value=val_key,
                style="Quiz.TRadiobutton",
                command=self._on_select
            )
            rb.pack(side="left")
            self.buttons[val_key] = rb
        self.feedback_lbl = tk.Label(
            self, 
            text="", 
            font=("Segoe UI", 11, "bold"),
            bg="white"
        )
        self.feedback_lbl.pack(pady=(0, 20))
    def _on_select(self):
        if self.answered: return
        self.answered = True
        choice = self.selected_var.get()
        correct = str(self.question_data["correct"])
        for btn in self.buttons.values():
            btn.configure(state="disabled")
        if choice == correct:
            self.feedback_lbl.config(text="✓ Correct!", fg="#27ae60") 
            self.on_answer(True)
        else:
            opts = self.question_data["options"]
            if isinstance(opts, dict):
                correct_text = opts.get(correct, correct)
            elif isinstance(opts, list) and correct.isdigit():
                idx = int(correct)
                correct_text = opts[idx] if 0 <= idx < len(opts) else correct
            else:
                correct_text = correct
            self.feedback_lbl.config(text=f"✗ Incorrect. Answer: {correct_text}", fg="#c0392b") 
            self.on_answer(False)
class StudyBuddyWorkspace(BaseWorkspace):
    def __init__(self, parent, supervisor, colors):
        super().__init__(parent, supervisor)
        self.colors = colors if colors else {
            "bg_main": "#f0f0f0",
            "accent": "#6c5ce7",
            "text_primary": "#2d3436",
            "text_secondary": "#636e72"
        }
        self.current_pdf = None
        self.quiz_state = None
        self._build_ui()
    def _build_ui(self):
        self.config(bg=self.colors["bg_main"])
        header = tk.Frame(self, bg=self.colors["bg_main"])
        header.pack(fill="x", padx=40, pady=(30, 20))
        tk.Label(
            header,
            text="Study Buddy",
            font=("Segoe UI", 20, "bold"),
            bg=self.colors["bg_main"],
            fg=self.colors["text_primary"]
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Upload materials, ask questions, or take interactive quizzes.",
            font=("Segoe UI", 11),
            bg=self.colors["bg_main"],
            fg=self.colors["text_secondary"]
        ).pack(anchor="w", pady=(5, 0))
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=self.colors["bg_main"], sashwidth=4)
        paned.pack(fill="both", expand=True, padx=40, pady=10)
        left_panel = tk.Frame(paned, bg=self.colors["bg_main"])
        paned.add(left_panel, minsize=350, width=400)
        self._build_upload_card(left_panel)
        self._build_action_card(left_panel)
        self.right_panel = tk.Frame(paned, bg=self.colors["bg_main"])
        paned.add(self.right_panel, stretch="always")
        self.view_container = tk.Frame(self.right_panel, bg="white", bd=1, relief="solid")
        try: self.view_container.config(highlightbackground="#E5E5E5", highlightthickness=1, bd=0)
        except: pass
        self.view_container.pack(fill="both", expand=True)
        self.text_output = scrolledtext.ScrolledText(
            self.view_container,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            bg="white",
            fg="#333",
            padx=30, pady=30,
            bd=0,
            state="disabled"
        )
        self.text_output.tag_config("bold", font=("Segoe UI", 11, "bold"))
        self.quiz_container = tk.Frame(self.view_container, bg="white")
        self.text_output.place(relx=0, rely=0, relwidth=1, relheight=1)
    def _build_upload_card(self, parent):
        card = tk.Frame(parent, bg="white", padx=20, pady=20)
        card.pack(fill="x", pady=(0, 15))
        try: card.config(highlightbackground="#E5E5E5", highlightthickness=1)
        except: pass
        tk.Label(card, text="1. Source Material", font=("Segoe UI", 11, "bold"), bg="white", fg=self.colors["text_primary"]).pack(anchor="w", pady=(0, 10))
        row = tk.Frame(card, bg="white")
        row.pack(fill="x")
        self.upload_btn = tk.Button(
            row,
            text="📄 Upload PDF",
            command=self._upload_pdf,
            bg="#ecf0f1",
            fg="#2c3e50",
            font=("Segoe UI", 10),
            relief="flat",
            padx=15, pady=5,
            cursor="hand2"
        )
        self.upload_btn.pack(side="left")
        self.file_lbl = tk.Label(row, text="No PDF loaded", font=("Segoe UI", 9, "italic"), bg="white", fg="#95a5a6", padx=10)
        self.file_lbl.pack(side="left")
    def _build_action_card(self, parent):
        card = tk.Frame(parent, bg="white", padx=20, pady=20)
        card.pack(fill="x")
        try: card.config(highlightbackground="#E5E5E5", highlightthickness=1)
        except: pass
        tk.Label(card, text="2. Learning Mode", font=("Segoe UI", 11, "bold"), bg="white", fg=self.colors["text_primary"]).pack(anchor="w", pady=(0, 10))
        tk.Label(card, text="Topic / Concept:", font=("Segoe UI", 10), bg="white", fg=self.colors["text_secondary"]).pack(anchor="w")
        self.topic_entry = tk.Entry(card, font=("Segoe UI", 11), bg="#f9f9f9", bd=1, relief="solid")
        self.topic_entry.pack(fill="x", pady=(5, 15), ipady=5)
        self.mode_var = tk.StringVar(value="EXPLAIN")
        modes_frame = tk.Frame(card, bg="white")
        modes_frame.pack(fill="x", pady=(0, 15))
        style = ttk.Style()
        style.configure("TRadiobutton", background="white", font=("Segoe UI", 10))
        for text, val in [("Explain", "EXPLAIN"), ("Summarize", "SUMMARIZE"), ("Quiz Me", "QUIZ")]:
            ttk.Radiobutton(modes_frame, text=text, variable=self.mode_var, value=val, style="TRadiobutton").pack(side="left", padx=(0, 15))
        self.run_btn = tk.Button(
            card,
            text="Run Action",
            command=self._on_run,
            bg=self.colors["accent"],
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            padx=20, pady=10,
            cursor="hand2"
        )
        self.run_btn.pack(fill="x")
    def _upload_pdf(self):
        path = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
        if path:
            self.current_pdf = path
            filename = path.split("/")[-1]
            self.file_lbl.config(text=f"✓ {filename}", fg=self.colors["accent"])
            try:
                self.supervisor.set_uploaded_file(path)
            except Exception as e:
                pass
    def _on_run(self):
        topic = self.topic_entry.get().strip()
        mode = self.mode_var.get()
        if not self.current_pdf and not topic:
            messagebox.showwarning("Input Missing", "Please upload a PDF or enter a topic.")
            return
        self.run_btn.config(state="disabled", text="Processing...")
        self.update_idletasks()
        threading.Thread(target=self._execute_pipeline, args=(mode, topic), daemon=True).start()
    def _execute_pipeline(self, mode, topic):
        try:
            if mode == "QUIZ":
                if not generate_quiz:
                    raise Exception("Backend module 'study_buddy.pipelines.quiz_generator' not found.")
                input_mode = "PDF_ONLY" if self.current_pdf else "PROMPT_ONLY"
                pdf_path = self.current_pdf or ""
                if build_study_context:
                    study_context = build_study_context(input_mode, prompt=topic, pdf_path=pdf_path)
                else:
                    study_context = topic
                quiz_data = generate_quiz(study_context)
                self.after(0, self._start_quiz, quiz_data)
            else:
                prompt_text = f"{mode.lower()} {topic}"
                result = self.supervisor.handle_user_input(prompt_text)
                response = result.get("response", "Error occurred.")
                self.after(0, self._show_text_result, response)
        except Exception as e:
            self.after(0, self._show_error, str(e))
    def _show_text_result(self, text):
        self.quiz_container.place_forget()
        self.text_output.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.text_output.config(state="normal")
        self.text_output.delete("1.0", "end")
        self.text_output.insert("1.0", text)
        self.text_output.config(state="disabled")
        self._reset_ui()
    def _show_error(self, msg):
        self._show_text_result(f"Error: {msg}")
        self._reset_ui()
    def _reset_ui(self):
        self.run_btn.config(state="normal", text="Run Action")
    def _start_quiz(self, quiz_data):
        self._reset_ui()
        if QuizState:
            self.quiz_state = QuizState(quiz_data["questions"])
        else:
            class MockState:
                def __init__(self, questions):
                    self.questions = questions
                    self.current = 0
                    self.score = 0
                def current_question(self):
                    return self.questions[self.current]
            self.quiz_state = MockState(quiz_data["questions"])
        self.text_output.place_forget()
        self.quiz_container.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._render_question()
    def _render_question(self):
        for w in self.quiz_container.winfo_children():
            w.destroy()
        if self.quiz_state.current >= len(self.quiz_state.questions):
            self._show_quiz_score()
            return
        header = tk.Frame(self.quiz_container, bg="white")
        header.pack(fill="x", padx=30, pady=20)
        tk.Label(
            header,
            text=f"Question {self.quiz_state.current + 1} of {len(self.quiz_state.questions)}",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["accent"],
            bg="white"
        ).pack(side="left")
        tk.Label(
            header,
            text=f"Score: {self.quiz_state.score}",
            font=("Segoe UI", 10),
            fg=self.colors["text_secondary"],
            bg="white"
        ).pack(side="right")
        q_data = self.quiz_state.current_question()
        q_frame = QuestionFrame(self.quiz_container, q_data, self._on_answer_submit, self.colors)
        q_frame.pack(fill="x", padx=30, pady=10)
        self.next_btn = tk.Button(
            self.quiz_container,
            text="Next Question ➜",
            command=self._next_question,
            state="disabled",
            bg="#ecf0f1",
            fg="#95a5a6",
            relief="flat",
            font=("Segoe UI", 10),
            padx=15, pady=8
        )
        self.next_btn.pack(anchor="e", padx=30, pady=10)
    def _on_answer_submit(self, is_correct):
        if is_correct:
            self.quiz_state.score += 1
        self.next_btn.config(state="normal", bg=self.colors["accent"], fg="white", cursor="hand2")
    def _next_question(self):
        self.quiz_state.current += 1
        self._render_question()
    def _show_quiz_score(self):
        for w in self.quiz_container.winfo_children():
            w.destroy()
        center = tk.Frame(self.quiz_container, bg="white")
        center.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(center, text="Quiz Completed! 🎉", font=("Segoe UI", 20, "bold"), bg="white", fg=self.colors["text_primary"]).pack(pady=10)
        score_txt = f"You scored {self.quiz_state.score} out of {len(self.quiz_state.questions)}"
        tk.Label(center, text=score_txt, font=("Segoe UI", 14), bg="white", fg=self.colors["text_secondary"]).pack(pady=5)
        tk.Button(
            center, 
            text="Back to Study Mode",
            command=lambda: self._show_text_result("Quiz finished. Ready for next task."),
            bg=self.colors["accent"],
            fg="white",
            relief="flat",
            padx=20, pady=10
        ).pack(pady=20)