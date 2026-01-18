# 🤖 Student Academic & Career Assistant

---

> AI-powered Multi-Agent System ✨

> A comprehensive AI assistant platform powered by multiple specialized agents for ***chat***, ***study***, ***transcription***, ***resume building***, and ***website generation***.

---

## 🎯 Introduction

### Overview

The **Student Academic & Career Assistant** is a modular desktop application that orchestrates multiple specialized AI agents. Unlike standard chatbots, this system uses a Supervisor-Agent pattern. A central supervisor routes user intent to specific experts-whether for deep academic research, audio transcription, resume creation, or website prototyping-ensuring high-quality, domain-specific results.

### Problem Statement

In today's digital landscape, users need diverse AI capabilities but often have to switch between multiple applications:
- Students need study assistance, note-taking, and quiz generation
- Professionals require resume building and editing tools
- Developers want automated website generation
- Everyone needs intelligent chat capabilities with web search

This project solves these problems by providing a **unified, intelligent platform** where specialized AI agents work together seamlessly.

### What This Project Does

This system provides five core functionalities through specialized agents:

1. **💬  `General Chat Agent`** : Intelligent conversational AI with web search capabilities
2. **📚  `Study Buddy Agent`** : PDF analysis, explanations, summaries, and quiz generation
3. **🎙️  `Voice-to-Notes Agent`** : Audio transcription and automated lecture note generation
4. **📄  `Resume Builder Agent`** : AI-powered resume creation with professional DOCX formatting
5. **🌐  `Website Builder Agent`** : Natural language to website generation

All agents are integrated with a **centralized logging system** for debugging, monitoring, and comprehensive audit trails.

---

## 📸 Screenshots

<table>
  <tr>
    <td width="33%">
      <img src="https://github.com/Priyash-Das/Photos/blob/main/Student-Academic-Career-Assistant/1.png" alt="Preview 1" width="100%">
      <p align="center">Study Buddy Agent (EXPLAIN)</p>
    </td>
    <td width="33%" rowspan="4">
      <img src="https://github.com/Priyash-Das/Photos/blob/main/Student-Academic-Career-Assistant/4.png" alt="Preview 4" height="100%">
      <p align="center">General Chat Agent</p>
    </td>
    <td width="33%">
      <img src="https://github.com/Priyash-Das/Photos/blob/main/Student-Academic-Career-Assistant/2.png" alt="Preview 5" width="100%">
      <p align="center">Study Buddy Agent (QUIZ)</p>
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/Priyash-Das/Photos/blob/main/Student-Academic-Career-Assistant/3.png" alt="Preview 7" width="100%">
      <p align="center">Resume Builder Agent</p>
    </td>
    <td>
      <img src="https://github.com/Priyash-Das/Photos/blob/main/Student-Academic-Career-Assistant/5.png" alt="Preview 6" width="100%">
      <p align="center">Website Builder Agent</p>
    </td>
  </tr>
  <tr>
    <td>
      <img src="https://github.com/Priyash-Das/Photos/blob/main/Student-Academic-Career-Assistant/6.png" alt="Preview 2" width="100%">
      <p align="center">Voice-to-Notes Agent</p>
    </td>
    <td>
      <img src="https://github.com/Priyash-Das/Photos/blob/main/Student-Academic-Career-Assistant/7.png" alt="Preview 3" width="100%">
      <p align="center">Centralized Log Viewer</p>
    </td>
  </tr>
</table>

---

## 🎬 Demo

### Video Walkthrough
[📺 Watch Full Demo](#) *(will-soon)*

### More Screenshots
- [Chat Agent](#)
- [Study Buddy](#)
- [Audio to Lecture Notes](#)
- [Resume Builder](#)
- [Website Builder](#)

---

## ⭐ Core Features

### 1. 💬 General Chat Agent

The chat agent provides intelligent, context-aware conversations with advanced capabilities:

**Key Features:**
- **Multi-Model Support**: Uses Gemini 2.5 Flash (default/fast), Llama 3.3 70B (deep thinking), and fallback models
- **Web Search Integration**: Real-time information retrieval via SerpAPI
- **Conversational Memory**: Maintains context across multiple conversation turns
- **Smart Model Switching**: Automatically uses appropriate models based on query complexity
- **Interactive UI**: Clean Tkinter interface with scrollable chat history
- **Mode Selection**: Toggle between FAST and DEEP thinking modes

**Technical Implementation:**

> Primary Models:
> - Default/Fast: gemini-2.5-flash (fast, efficient)
> - Deep: llama-3.3-70b-versatile (complex reasoning)
> - Fallback: tencent/WeDLM-8B-Instruct (error handling)


**Use Cases:**
- General knowledge questions
- Research and fact-checking with web search
- Creative writing assistance
- Code explanations
- Problem-solving discussions

---

### 2. 📚 Study Buddy Agent

An AI-powered study assistant that transforms PDF documents into interactive learning materials.

**Key Features:**
- **PDF Document Upload**: Support for academic papers, textbooks, and study materials
- **Text Extraction**: Intelligent PDF parsing
- **Document Analysis**: Uses Qwen 2.5 7B for comprehensive reading
- **Concept Explanation**: Detailed explanations using Llama 3.3 70B
- **Smart Summarization**: Gemini 2.5 Flash for concise summaries
- **Quiz Generation**: Automatic multiple-choice quiz creation

**Technical Implementation:**

> Specialized Models for Each Task:
> - Reader: Qwen/Qwen2.5-7B-Instruct (document comprehension)
> - Explainer: llama-3.3-70b-versatile (deep explanations)
> - Summarizer: gemini-2.5-flash (concise summaries)
> - Quiz Generator: gemini-2.5-flash (question generation)

**Workflow:**
1. User uploads PDF document
2. Document is parsed and text extracted
3. User can request:
   - Full document summary
   - Concept explanations
   - Quiz generation (5+ questions with answers)

**Output Examples:**
- **Summaries**: Key points, main arguments, conclusions
- **Explanations**: Detailed breakdowns with examples and context
- **Quizzes**: Multiple-choice questions with correct answers highlighted

---

### 3. 🎙️ Voice-to-Notes Agent

Transform audio recordings into structured, searchable lecture notes with AI enhancement.

**Key Features:**
- **Audio Transcription**: Uses Whisper Large V3 for accurate speech-to-text
- **Format Support**: MP3, WAV, M4A, and other common audio formats
- **Lecture Note Generation**: Automatically structures transcriptions into organized notes
- **Interactive Q&A**: Ask questions about transcribed content using Llama 3.3 70B
- **Text Export**: Save transcriptions and notes to text files
- **Status Tracking**: Real-time progress indicators

**Technical Implementation:**

> Processing Pipeline:
> - Audio Upload → Whisper Large V3 (via Groq API - transcription)
> - Raw Transcription → Gemini 1.5 Flash (note formatting)
> - Structured Notes → Llama 3.3 70B (Q&A capability)

**Note Formatting:**
- Headers and logical sections
- Bullet points for key concepts
- Definitions and explanations
- Summary sections
- Structured, readable format

**Use Cases:**
- Lecture recordings → Study notes
- Meeting recordings → Action items
- Podcast transcription → Searchable text
- Interview transcription → Structured summaries

---

### 4. 📄 Resume Builder Agent

Professional resume generation powered by AI with ATS-optimized formatting and DOCX export.

**Key Features:**
- **Natural Language Input**: Describe your experience in plain text
- **Intelligent Parsing**: Extracts key information automatically using Llama 3.3 70B
- **Professional DOCX Output**: ATS-friendly Microsoft Word format
- **Structured Data Model**: Validates all resume sections
- **Section-by-Section Editing**: Edit Assistant for modifications
- **Comprehensive Validation**: Ensures data completeness and formatting

**Resume Sections:**
- **Header**: Name, email, phone, address, LinkedIn, portfolio
- **Professional Summary**: Career overview and key strengths
- **Work Experience**: Role, company, dates, location, bullet points
- **Education**: Degree, institution, year, GPA (optional)
- **Skills**: 
  - Programming languages
  - Frameworks and libraries
  - Tools and technologies
- **Projects**: Title, description, technologies, links
- **Hobbies**
- **Certifications**: Name, issuer, date

**Technical Implementation:**

> Processing Flow:
> - User Input → Prompt Processing → LLM Generation (Llama 3.3) 
> - Validation → DOCX Rendering → Output File

> Components:
>  - ResumeAgent: LLM-powered content generation
>  - ResumeValidator: Ensures data completeness
>  - DocxRenderer: Professional formatting engine

> Data Model:
> class ResumeData:
>    - header: PersonalInfo (name, email, phone, address, links)
>    - summary: str (professional summary)
>    - experience: List[Experience] (work history)
>    - education: List[Education] (academic background)
>    - skills: SkillSet (categorized skills)
>    - projects: List[Project] (optional)
>    - hbbies: List[Hobbie] (optional)
>    - certifications: List[Certification] (optional)

**Output Quality:**
- ATS-compatible formatting
- Professional typography
- Consistent styling
- Proper section hierarchy
- Bullet point optimization
- Microsoft Word .docx format

---

### 5. 🌐 Website Builder Agent

Generate complete, responsive websites from natural language descriptions.

**Key Features:**
- **Natural Language Input**: Describe your website in plain text
- **Intelligent Spec Inference**: Automatically determines website type and features
- **Full HTML Generation**: Creates complete, self-contained HTML files
- **Style Customization**: Modify design through natural language
- **Live Preview**: Open generated websites in browser instantly
- **Export Options**: Copy code or download as HTML file
- **Error Handling**: Comprehensive validation and sanitization

**Website Types Supported:**
- Landing pages
- Portfolios
- Business websites
- Product showcases
- Event pages
- Personal blogs
- Contact pages
- Etc

**Technical Implementation:**

> Processing Pipeline:
> - User Prompt → Spec Inference → LLM Generation (Llama 3.3) 
> - HTML Sanitization → Validation → Output

**Generated Code Features:**
- Responsive design (mobile-friendly)
- Modern CSS styling (inline styles)
- Clean, semantic HTML5
- Cross-browser compatible
- Self-contained (no external dependencies)
- Customizable via modification prompts

**Workflow:**
1. User describes desired website
2. System infers website specifications
3. LLM generates complete code
4. Output is sanitized and validated
5. User can preview, modify, or export

---

## 🏗️ Architecture & Project Structure

### High-Level Architecture

```
        ┌─────────────────────────────────────────────────────────────┐
        │                   User Interface (Tkinter)                  │
        │             ui/app.py – Unified Desktop Application         │
        └───────────────────────────────┬─────────────────────────────┘
                                        │
        ┌───────────────────────────────┴─────────────────────────────┐
        │                   Supervisor Agent Layer                    │
        │        supervisor/supervisor_agent.py – Orchestration       │
        └───┬─────────┬───────────────┬───────────────┬──────────┬────┘
            │         │               │               │          │
┌───────────▼┐ ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼───────┐ ┌▼──────────────┐
│ Chat Agent │ │ Study Buddy │ │ Voice Notes │ │ Resume Agent │ │ Website Agent │
└────────────┘ └─────────────┘ └─────────────┘ └──────────────┘ └───────────────┘

```

### Directory Structure

```
Student-Academic-&-Career-Assistant/
├─ .env
├─ agents
│  ├─ resume_agent.py
│  ├─ study_buddy_agent.py
│  ├─ voice_notes_agent.py
│  └─ website_agent.py
├─ ai_chatbot
│  ├─ .env
│  ├─ config
│  │  ├─ models.py
│  │  └─ settings.py
│  ├─ controller
│  │  ├─ chat_controller.py
│  │  ├─ fallback_controller.py
│  │  ├─ mode_controller.py
│  │  └─ session_manager.py
│  ├─ intelligence
│  │  ├─ context_manager.py
│  │  ├─ memory_summarizer.py
│  │  ├─ prompt_builder.py
│  │  ├─ query_classifier.py
│  │  ├─ system_tools.py
│  │  ├─ tool_router.py
│  │  ├─ web_search.py
│  │  └─ web_summarizer.py
│  ├─ llm
│  │  ├─ base_client.py
│  │  ├─ deep_model.py
│  │  ├─ fallback_model.py
│  │  └─ fast_model.py
│  ├─ requirements.txt
│  ├─ utils
│  │  ├─ clipboard.py
│  │  └─ error_handler.py
│  └─ __init__.py
├─ logs
│  ├─ app_2026-00-00_00-00-00.log
│  └─ archive
├─ resume_builder
│  ├─ .env
│  ├─ config
│  │  ├─ models.py
│  │  ├─ prompts.py
│  │  ├─ settings.py
│  │  └─ __init__.py
│  ├─ core
│  │  ├─ resume_agent.py
│  │  ├─ resume_editor.py
│  │  ├─ resume_schema.py
│  │  ├─ resume_state.py
│  │  ├─ resume_validator.py
│  │  └─ __init__.py
│  ├─ llm
│  │  ├─ groq_client.py
│  │  ├─ llm_router.py
│  │  └─ __init__.py
│  ├─ renderer
│  │  ├─ docx_renderer.py
│  │  ├─ layout_constants.py
│  │  └─ __init__.py
│  ├─ requirements.txt
│  └─ __init__.py
├─ study_buddy
│  ├─ .env
│  ├─ config
│  │  ├─ models.py
│  │  └─ settings.py
│  ├─ core
│  │  ├─ chunker.py
│  │  ├─ context_builder.py
│  │  ├─ input_handler.py
│  │  ├─ pdf_loader.py
│  │  └─ quiz_state.py
│  ├─ llm
│  │  ├─ client.py
│  │  └─ prompts.py
│  ├─ pipelines
│  │  ├─ explain.py
│  │  ├─ quiz.py
│  │  ├─ quiz_generator.py
│  │  └─ summarize.py
│  ├─ requirements.txt
│  ├─ utils
│  │  ├─ clipboard.py
│  │  ├─ errors.py
│  │  └─ status.py
│  └─ __init__.py
├─ supervisor
│  ├─ adapters
│  │  └─ chat_adapter.py
│  ├─ execution_router.py
│  ├─ intent_classifier.py
│  ├─ schemas.py
│  ├─ shared_memory.py
│  ├─ supervisor_agent.py
│  └─ __init__.py
├─ ui
│  ├─ app.py
│  ├─ chat_area.py
│  ├─ header.py
│  ├─ log_viewer.py
│  ├─ main_window.py
│  ├─ sidebar.py
│  ├─ status_bar.py
│  ├─ theme.py
│  ├─ workspace
│  │  ├─ base.py
│  │  ├─ chat_workspace.py
│  │  ├─ resume_workspace.py
│  │  ├─ study_buddy_workspace.py
│  │  ├─ voice_notes_workspace.py
│  │  └─ website_workspace.py
│  └─ __init__.py
├─ utils
│  ├─ logger.py
│  ├─ log_manager.py
│  └─ __init__.py
├─ voice_to_notes_generator
│  ├─ .env
│  ├─ assets
│  │  └─ temp_audio
│  ├─ config
│  │  ├─ models.py
│  │  ├─ settings.py
│  │  └─ __init__.py
│  ├─ pipelines
│  │  ├─ audio_ingestion.py
│  │  ├─ explain_answer.py
│  │  ├─ notes_generator.py
│  │  ├─ notes_qa.py
│  │  ├─ transcription.py
│  │  └─ __init__.py
│  ├─ requirements.txt
│  ├─ state
│  │  ├─ lecture_state.py
│  │  └─ __init__.py
│  ├─ utils
│  │  ├─ chunking.py
│  │  ├─ docx_exporter.py
│  │  ├─ prompt_templates.py
│  │  ├─ safety.py
│  │  └─ __init__.py
│  └─ __init__.py
└─ website_builder
   ├─ .env
   ├─ config
   │  ├─ settings.py
   │  └─ __init__.py
   ├─ core
   │  ├─ error_handler.py
   │  ├─ generator.py
   │  ├─ health_check.py
   │  ├─ llm_client.py
   │  ├─ prompt_processor.py
   │  ├─ sanitizer.py
   │  ├─ spec_inference.py
   │  ├─ validator.py
   │  └─ __init__.py
   ├─ export
   │  ├─ copy_manager.py
   │  ├─ download_manager.py
   │  └─ __init__.py
   ├─ preview
   │  ├─ live_preview.py
   │  ├─ temp_site_manager.py
   │  └─ __init__.py
   ├─ requirements.txt
   ├─ utils
   │  ├─ file_utils.py
   │  └─ __init__.py
   └─ __init__.py
```

### Key Component Descriptions

#### **Supervisor (supervisor/)**:
- Entry point for the entire system
- The brain of the operation. It initializes all agents, manages shared memory (e.g., the currently uploaded PDF), and routes UI events to the correct handler.

#### **Agents (agents/)**:
- These are lightweight wrappers that expose the complex logic of the sub-modules (like resume_builder) to the Supervisor.

#### **App Start (ui/app.py)**:
- Entry point for the entire system

#### **Utils (utils/)**
- Contains the LogManager, which provides a thread-safe, singleton logger used by every component to write to a single log file and the UI Log Viewer.

---

## 🔄 Workflow & Data Flow

### General Chat Agent Flow

```
User Input
    ↓
[Chat View] → Validate Input
    ↓
[Chat Core] → Select Model (Default/Deep)
    ↓
┌─────────────┐
│ Web Search? │ (if needed)
└─────────────┘
    ↓ 
[Web Search API]
    ↓
[API Client] → Call Appropriate LLM (Gemini/Groq/HF)
    ↓
Response Processing
    ↓
[Chat View] → Display Response
    ↓
Conversation Log Updated
```

**Key Decision Points:**
1. **Model Selection**: Default/Fast mode uses Gemini 2.5 Flash; Deep mode uses Llama 3.3 70B
2. **Web Search**: Triggered for questions requiring current information
3. **Error Handling**: Falls back to alternative models on failure

---

### Study Buddy Agent Flow

```
PDF Upload / Topic
    ↓
[Study Buddy View] → File Selection
    ↓
[PDF Reader] → Extract Text
    ↓
Text Storage in Memory
    ↓
User Action Selection:
    │
    ├─ [Explainer] → Llama 3.3 70B → Detailed Explanation
    │
    ├─ [Summarizer] → Gemini 2.5 Flash → Summary Output
    │
    └─ [Quiz Generator] → Gemini 2.5 Flash → Quiz
    ↓
[Study Buddy View] → Display Result
    ↓
Conversation Log Updated
```

**Processing Steps:**
1. **Upload**: User selects PDF file or Write/Paste Topic
2. **Extraction**: Extracts all text
3. **Storage**: Text stored for multiple operations
4. **Operation**: User chooses summary, explanation, quiz
5. **LLM Call**: Appropriate model processes request
6. **Display**: Results shown in UI with proper formatting

---

### Voice to Notes Agent Flow

```
Audio File Upload
    ↓
[Voice to Notes View] → File Selection (MP3/WAV/M4A)
    ↓
[Transcriber] → Groq Whisper Large V3 API
    ↓
Raw Transcription Text
    ↓
[Lecture Notes Generator] → Gemini 1.5 Flash
    ↓
Structured Lecture Notes
    ↓
                    ┌──────────────┐
                    │ User Action  │
                    └──────────────┘
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
  Display Notes      Ask Question      Save to File
        ↓                 ↓                 ↓
 [Text Display]      [Notes Q&A]      [File Export] - [DOCX]
                          ↓
                     Llama 3.3 70B
                          ↓
                    Answer Display
```

**Processing Pipeline:**
1. **Transcription**: Audio → Text via Whisper
2. **Formatting**: Raw text → Structured notes via Gemini
3. **Interaction**: Q&A capability via Llama
4. **Export**: Save transcription and notes to docx file

---

### Resume Builder Agent Flow

```
User Input (Natural Language)
    ↓
[Resume Builder View] → Collect Form Data
    ↓
[Resume Agent Wrapper] → Convert to Prompt
    ↓
[Core Resume Agent] → Llama 3.3 70B Generation
    ↓
JSON Response
    ↓
[LLM Parser] → Parse JSON to ResumeData
    ↓
[Resume Validator] → Validate Required Fields
    ↓
Validated ResumeData Object
    ↓
[DOCX Renderer] → Format with python-docx
    ↓
generated_resume.docx
    ↓
                   ┌──────────────┐
                   │ User Action  │
                   └──────────────┘
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
   View Resume      Edit Section      Download DOCX
        ↓                 ↓                 ↓
  [Text Display]   [Editor Assist]    [File Export]
```

**Editor Assist Flow:**
```
User Selects Section (e.g., Experience)
    ↓
[Editor Assist View] → Display Current Content
    ↓
User Provides Modification Instructions
    ↓
[Resume Agent] → Llama 3.3 70B for Editing
    ↓
Updated Section Content
    ↓
[Resume Validator] → Re-validate
    ↓
[DOCX Renderer] → Re-render Resume
    ↓
Updated generated_resume.docx
```

**Data Transformation:**
1. **Input**: Natural language description
2. **Prompt**: Structured prompt with sections
3. **Generation**: LLM outputs JSON
4. **Parsing**: JSON → Python objects
5. **Validation**: Check required fields
6. **Rendering**: Objects → Formatted DOCX
7. **Output**: Professional resume docx file

---

### Website Builder Agent Flow

```
User Prompt Input
    ↓
[Prompt Processor] → Validate + Merge Prompts
    ↓
[Spec Inference] → Determine Website Type
    ↓
Website Specification
    ↓
[Generator] → Llama 3.3 70B HTML Generation
    ↓
Raw Code Output
    ↓
[Output Sanitizer] → Remove Markdown, Clean Code
    ↓
[HTML Validator] → Check Valid HTML
    ↓
[Health Check] → Final Quality Validation
    ↓
Clean, Valid HTML
    ↓
                   ┌─────────────┐
                   │ User Action │
                   └─────────────┘
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
   Live Preview       Copy Code         Download
        ↓                 ↓                 ↓
  [Browser Open]     [Clipboard]       [File Save] - [.html]
```

**Quality Pipeline:**
1. **Validation**: Check prompt is non-empty
2. **Inference**: Detect website type from description
3. **Generation**: LLM creates complete HTML
4. **Sanitization**: Remove markdown artifacts
5. **Validation**: Ensure valid HTML structure
6. **Health Check**: Final quality verification
7. **Output**: Ready-to-use HTML

---

## 💻 Technology Stack

### Core Languages & Frameworks

| Technology  | Version  | Purpose                      |
|-------------|----------|------------------------------|
| **Python**  | 3.10+    | Primary programming language |
| **Tkinter** | Built-in | Desktop GUI framework        |

### AI Models & Providers

#### **Google Gemini** (via Google AI SDK)
- `gemini-2.5-flash`: Fast chat, summarization, quiz generation
- `gemini-1.5-flash`: Lecture note formatting

#### **Groq** (via Groq API)
- `llama-3.3-70b-versatile`: Deep chat, explanations, resume generation, website generation, editing
- `whisper-large-v3`: Audio transcription

#### **Hugging Face** (Inference API)
- `Qwen/Qwen2.5-7B-Instruct`: PDF reading and comprehension
- `tencent/WeDLM-8B-Instruct`: Fallback chat model

### External APIs

| Service     | Purpose                  |
|-------------|--------------------------|
| **SerpAPI** | Web search functionality |

### Python Libraries

#### **Core Dependencies**
```txt
# Standard Library (Built-in, no installation required)

tkinter              # UI framework (built-in)
dataclasses          # Structured data models (Python 3.7+)
typing               # Type hints

# Third-Party Dependencies (install via pip)

# UI & Imaging
customtkinter        # Modern UI components for Tkinter
Pillow               # Image processing

# Utilities
python-dotenv        # Environment variable management

# Web & API
requests             # HTTP client for API calls

# AI Models / SDKs
google-generativeai  # Google Generative AI SDK
groq                 # Groq API client

# Document Processing
PyPDF2               # PDF text extraction
python-docx          # DOCX file generation

# Audio Processing
openai-whisper       # Audio transcription (Whisper model)
```

## 🚀 Setup & Installation

### Prerequisites

Before installing, ensure you have:

- **Python 3.10 or higher** installed
- **pip** (Python package installer)
- **Internet connection** for API access
- **API Keys** for:
  - Google Gemini
  - Groq
  - Hugging Face
  - SerpAPI

### Step 1: Clone the Repository

```bash
git clone https://github.com/Priyash-Das/Student-Academic-Career-Assistant-Agent.git
cd Student-Academic-&-Career-Assistant
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

Create a `requirements.txt` file:

```txt
# ai_chatbot/requirements.txt
`requests`
`python-dotenv`

# study_buddy/requirements.txt
`python-dotenv`
`requests`
`PyPDF2`

# voice_to_notes_generator/requirements.txt
`python-dotenv`
`google-generativeai`
`groq`
`python-docx`

# resume_builder/requirements.txt
`python-dotenv`
`requests`
`python-docx`
`customtkinter`
`Pillow`

# website_builder/requirements.txt
`requests`
`python-dotenv`
`groq`
```

Install dependencies:

```bash
pip install -r ai_chatbot/requirements.txt
pip install -r study_buddy/requirements.txt
pip install -r voice_to_notes_generator/requirements.txt
pip install -r resume_builder/requirements.txt
pip install -r website_builder/requirements.txt
```

### Step 4: ⚙️ Configuration (Configure Environment Variables)

Create `.env` / Rename `env.example.txt` to `.env`:

Edit `Student-Academic-&-Career-Assistant/.env` and add your API keys:

```env
# ===== GLOBAL KEYS =====
GOOGLE_API_KEY=your_google_api_key_here
HF_API_KEY=your_huggingface_token_here
GROQ_API_KEY=your_groq_api_key_here
SERPAPI_KEY=your_serpapi_key_here

# ===== CHAT AGENT =====
CHATBOT_DEFAULT=gemini-2.5-flash
CHATBOT_DEEP=llama-3.3-70b-versatile
CHATBOT_FALLBACK=tencent/WeDLM-8B-Instruct
# ===== STUDY BUDDY =====
STUDY_READER_MODEL=Qwen/Qwen2.5-7B-Instruct
STUDY_EXPLAIN_MODEL=llama-3.3-70b-versatile
STUDY_SUMMARY_MODEL=gemini-2.5-flash
STUDY_QUIZ_MODEL=gemini-2.5-flash
# ===== VOICE TO NOTES =====
TRANSCRIBE_MODEL=whisper-large-v3
LECTURE_NOTES_MODEL=gemini-1.5-flash
NOTES_QA_MODEL=llama-3.3-70b-versatile
# ===== RESUME =====
RESUME_GENERATION_MODEL=llama-3.3-70b-versatile
EDITOR_ASSIST_MODEL=llama-3.3-70b-versatile
# ===== WEBSITE =====
WEBSITE_MODEL=llama-3.3-70b-versatile
```

Edit `Student-Academic-&-Career-Assistant/ai_chatbot/.env` and add your API keys:

```env
GOOGLE_API_KEY=your_google_api_key_here
HF_API_KEY=your_huggingface_token_here
GROQ_API_KEY=your_groq_api_key_here
SERPAPI_KEY=your_serpapi_key_here

CHATBOT_DEFAULT=gemini-2.5-flash
CHATBOT_DEEP=llama-3.3-70b-versatile
CHATBOT_FALLBACK=tencent/WeDLM-8B-Instruct

MAX_RETRIES=1
REQUEST_TIMEOUT=30
MAX_CONTEXT_MESSAGES=10
```

Edit `Student-Academic-&-Career-Assistant/study_buddy/.env` and add your API keys:

```env
GOOGLE_API_KEY=your_google_api_key_here
HF_API_KEY=your_huggingface_token_here
GROQ_API_KEY=your_groq_api_key_here

STUDY_READER_MODEL=Qwen/Qwen2.5-7B-Instruct
STUDY_EXPLAIN_MODEL=llama-3.3-70b-versatile
STUDY_SUMMARY_MODEL=gemini-2.5-flash
STUDY_QUIZ_MODEL=gemini-2.5-flash
```
Edit `Student-Academic-&-Career-Assistant/voice_to_notes_generator/.env` and add your API keys:

```env
GOOGLE_API_KEY=your_google_api_key_here
HF_API_KEY=your_huggingface_token_here
GROQ_API_KEY=your_groq_api_key_here

TRANSCRIBE_MODEL=whisper-large-v3
LECTURE_NOTES_MODEL=gemini-1.5-flash
NOTES_QA_MODEL=llama-3.3-70b-versatile
```

Edit `Student-Academic-&-Career-Assistant/resume_builder/.env` and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here

RESUME_GENERATION_MODEL=llama-3.3-70b-versatile
EDITOR_ASSIST_MODEL=llama-3.3-70b-versatile
```

Edit `Student-Academic-&-Career-Assistant/website_builder/.env` and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key_here

WEBSITE_MODEL=llama-3.3-70b-versatile
```

### Step 5: Run the Application

```bash
python -m ui.app
```

The main application window should appear.

---

## 🔮 Future Improvements - Version 1.0.0 (Current)

> ### Planned Features:
> #### **Phase 1: Enhanced Capabilities** > **Phase 2: Advanced Features** > **Phase 3: Collaboration & Cloud** > **Phase 4: Enterprise Features**

> ### Performance Optimizations + UI/UX Enhancements + Agent Expansions + Integration Plans + Cross Platform Compatibility

---

## 🎉 Conclusion & Final Thoughts

#### The Student Academic & Career Assistant (AI Multi-Agent System) successfully consolidates fragmented productivity workflows into a unified, intelligent platform by leveraging a robust Supervisor-Agent architecture. By orchestrating specialized models-ranging from Gemini Flash for rapid summarization to Llama 3.3 for complex reasoning-the system delivers a seamless user experience that balances high performance with cost-efficiency. Ultimately, this project serves as a practical blueprint for building scalable, local-first multi-agent systems, empowering users to streamline their academic and professional development through the power of collaborative AI.

---
# Thank you.
---
