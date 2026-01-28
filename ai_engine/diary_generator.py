import subprocess
import tempfile
import os
from datetime import date

from utils.config import INTERNSHIP_START_DATE, COMPANY_NAME
from ai_engine.decision_log import build_decision_log


# -------------------------------------------------
# ✅ WINDOWS-SAFE OLLAMA RUNNER (FILE REDIRECTION)
# -------------------------------------------------
def run_ollama(prompt: str) -> str:
    """
    Robust Ollama invocation for Windows + Python 3.13.
    Handles empty stdout cases gracefully.
    """

    result = subprocess.run(
        ["ollama", "run", "mistral", prompt],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=180,
    )

    stdout = (result.stdout or "").strip()
    stderr = (result.stderr or "").strip()

    # 🟢 Primary output
    if stdout:
        return stdout

    # 🟡 Fallback: Ollama sometimes writes here
    if stderr:
        return stderr

    # 🔴 True failure
    raise RuntimeError(
        "❌ Ollama produced no output on stdout or stderr.\n"
        "Check if Ollama service is running."
    )


# -------------------------------------------------
# DATE LOGIC
# -------------------------------------------------
def _is_first_day() -> bool:
    return date.today() == INTERNSHIP_START_DATE


# -------------------------------------------------
# GENERATORS
# -------------------------------------------------
def generate_work_summary(notes: str, input_mode: str) -> tuple[str, dict]:
    first_day = _is_first_day()

    context_block = (
        f"""
This is the FIRST DAY of the internship at {COMPANY_NAME}.
Focus on orientation, onboarding, and organizational exposure.
"""
        if first_day
        else f"""
This is a ROUTINE WORKING DAY of the internship at {COMPANY_NAME}.
Focus on assigned tasks and continuity of work.
Avoid onboarding content.
"""
    )

    prompt = f"""
You are helping a VTU B.E. student write the "What I worked on" section
of an internship diary.

{context_block}

Rules:
- First person
- Formal academic tone
- 80–120 words
- Tasks and exposure only
- No learning outcomes

Notes:
{notes}

Return only the work summary text.
"""

    work_summary = run_ollama(prompt)

    decision_log = build_decision_log(
        is_first_day=first_day,
        input_mode=input_mode,
    )

    return work_summary, decision_log


def generate_learnings(notes: str, decision_log: dict) -> str:
    first_day = decision_log["day_type"] == "FIRST_DAY"

    learning_context = (
        "Focus on initial understanding and professional awareness."
        if first_day
        else "Focus on skills strengthened and practical learning."
    )

    prompt = f"""
You are helping a VTU B.E. student write the "Learnings / Outcomes" section.

{learning_context}

Rules:
- First person
- Formal academic tone
- 50–80 words
- Skills and understanding only
- Do not repeat tasks

Notes:
{notes}

Return only the learning outcomes text.
"""

    return run_ollama(prompt)
