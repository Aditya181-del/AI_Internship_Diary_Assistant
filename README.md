# AI Internship Diary Assistant

A desktop GUI assistant that helps automate **VTU Internship Diary**
management using AI-assisted content generation, browser automation,
and reminder notifications — while preserving **human approval and control**.

This is a real, daily-use assistant designed around academic integrity,
system reliability, and real-world constraints.

---

## Overview

The assistant helps a VTU B.E. student to:

- Generate meaningful daily internship diary entries using local AI
- Track internship progress locally
- Receive reminders to fill the diary
- Assist (not blindly automate) VTU InternYet portal submissions

The system intentionally follows a **human-in-the-loop** design:
AI suggests → user reviews → user submits.

---

## Key Features

- 🖥️ Tkinter-based desktop GUI
- ✍️ AI-generated work summaries & learning outcomes
- 🧠 Explainable AI decision logging
- 🌐 Automated VTU InternYet portal filling (Playwright)
- ⏰ Reminder assistant (Email + WhatsApp)
- 📊 Local SQLite storage for progress tracking
- 🛑 Graceful fallback to full manual control

---

## Assistant Capabilities

Beyond diary generation, this project also functions as a **personal internship assistant**:

- Reminds the user to fill the diary on scheduled days
- Sends notifications via:
  - Email (SMTP)
  - WhatsApp (Twilio – optional)
- Ensures consistency across the internship duration
- Prevents missed diary entries due to forgetfulness

All reminder features are **optional** and configurable via environment variables.

---

## Tech Stack

- Python 3.13
- Tkinter (desktop GUI)
- SQLite (local persistence)
- Playwright (browser automation)
- Ollama (local LLM inference)
- SMTP (email reminders)
- Twilio (WhatsApp reminders – optional)

---

## System Requirements

- Windows 10 / 11
- Python 3.13+
- Ollama installed and running locally
- Internet access (for VTU InternYet portal & notifications)

---

## How to Run (No Coding Required)

1. Extract the project ZIP
2. Ensure Python and Ollama are installed
3. Configure environment variables (see below)
4. Double-click:

   **`run_app.bat`**

The GUI will launch automatically.

---
