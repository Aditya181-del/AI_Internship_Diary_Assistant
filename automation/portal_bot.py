import sys
import os
import time
import json
from datetime import date
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, TimeoutError

# -------------------------------------------------
# 🔧 TRUST WORKING DIRECTORY (GUI sets cwd)
# -------------------------------------------------
PROJECT_ROOT = os.getcwd()
sys.path.insert(0, PROJECT_ROOT)

from ai_engine.diary_generator import (
    generate_work_summary,
    generate_learnings,
)

# -------------------------------------------------
# 🔐 Load credentials
# -------------------------------------------------
load_dotenv()

INTERNYET_URL = "https://vtu.internyet.in/sign-in"
EMAIL = os.getenv("INTERNYET_EMAIL")
PASSWORD = os.getenv("INTERNYET_PASSWORD")

if not EMAIL or not PASSWORD:
    raise RuntimeError("❌ INTERNYET_EMAIL or INTERNYET_PASSWORD missing in .env")


# -------------------------------------------------
# 🧠 Helpers
# -------------------------------------------------
def wait_for_flag(path: str, label: str):
    print(f"⏸ Waiting for {label}...")
    while not os.path.exists(path):
        time.sleep(0.5)
    print(f"✅ {label} received.")


def suggest_skills(text: str):
    keywords = [
        "Python",
        "Data Science",
        "Data Analysis",
        "Machine Learning",
        "Statistics",
        "Problem Solving",
        "NumPy",
        "Pandas",
        "AI",
    ]
    return [k for k in keywords if k.lower() in text.lower()]


# -------------------------------------------------
# 🚀 MAIN LOGIC
# -------------------------------------------------
def ai_fill_diary(notes: str):
    automation_dir = os.path.join(PROJECT_ROOT, "automation")
    os.makedirs(automation_dir, exist_ok=True)

    ready_flag = os.path.join(automation_dir, "PORTAL_READY.flag")
    approval_flag = os.path.join(automation_dir, "APPROVAL_OK.flag")
    done_flag = os.path.join(automation_dir, "USER_DONE.flag")
    decision_log_path = os.path.join(automation_dir, "LAST_DECISION_LOG.json")
    input_mode_path = os.path.join(automation_dir, "INPUT_MODE.flag")

    # ---- Cleanup old flags ----
    for f in (ready_flag, approval_flag, done_flag, decision_log_path):
        if os.path.exists(f):
            os.remove(f)

    # ---- Read input mode ----
    input_mode = "text"
    if os.path.exists(input_mode_path):
        with open(input_mode_path, "r", encoding="utf-8") as f:
            input_mode = f.read().strip()

    today_day = str(date.today().day)

    with sync_playwright() as p:
        # ✅ DO NOT hardcode executable_path
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # ---------------- LOGIN ----------------
        page.goto(INTERNYET_URL, timeout=60000)
        page.fill("input[placeholder='Enter your email address']", EMAIL)
        page.fill("input[placeholder='Enter your password']", PASSWORD)
        page.click("button:has-text('Sign In')")
        page.wait_for_timeout(5000)

        # ---------------- VTU NOTICE ----------------
        try:
            page.click("button:has-text('I Understand')", timeout=5000)
            page.wait_for_timeout(1500)
        except TimeoutError:
            pass

        # ---------------- DIARY NAVIGATION ----------------
        page.click("text=Internship Diary")
        page.wait_for_timeout(4000)

        page.click("text=Choose internship")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)

        try:
            page.locator("input[placeholder='Pick a Date'] + button").click()
            page.wait_for_timeout(800)
            page.locator(f"button:has-text('{today_day}')").first.click()
            page.wait_for_timeout(800)
        except Exception:
            pass

        print("🟢 Date confirmed on VTU portal.")

        # ---- Signal GUI ----
        with open(ready_flag, "w", encoding="utf-8") as f:
            f.write("READY")

        # ---- Wait for GUI approval ----
        wait_for_flag(approval_flag, "GUI approval")

        # ---------------- AI GENERATION ----------------
        work_summary, decision_log = generate_work_summary(notes, input_mode)
        learnings = generate_learnings(notes, decision_log)

        with open(decision_log_path, "w", encoding="utf-8") as f:
            json.dump(decision_log, f, indent=2)

        skills = suggest_skills(work_summary + " " + learnings)

        # ---------------- FORM FILL ----------------
        page.fill("textarea[placeholder*='work']", work_summary)
        page.fill("textarea[placeholder*='learn']", learnings)

        print("✅ Diary content auto-filled.")
        print("⚠️ Manual steps remaining:")
        print("• Enter hours")
        print("• Add skills:", ", ".join(skills))
        print("• Review and SUBMIT manually")

        # ---- Wait until user confirms submission ----
        wait_for_flag(done_flag, "user submission")

        print("👋 Submission confirmed. Browser will remain open.")
        time.sleep(999999)  # keep browser alive intentionally


# -------------------------------------------------
# ENTRY
# -------------------------------------------------
if __name__ == "__main__":
    notes_file = os.path.join(PROJECT_ROOT, "automation", "NOTES.txt")

    if not os.path.exists(notes_file):
        raise RuntimeError("❌ NOTES.txt not found")

    with open(notes_file, "r", encoding="utf-8") as f:
        notes = f.read().strip()

    if not notes:
        raise RuntimeError("❌ Notes are empty")

    ai_fill_diary(notes)
