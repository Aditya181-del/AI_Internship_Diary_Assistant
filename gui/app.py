import os

# MUST be first
os.environ["PYTHONUTF8"] = "1"

import sys
import tkinter as tk

# -------------------------------------------------
# 🔧 Project root
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# -------------------------------------------------
# ✅ CRITICAL: Initialize DB before GUI loads
# -------------------------------------------------
from utils.db import init_db
from gui.dashboard import Dashboard


def main():
    # ✅ ENSURE DATABASE + TABLE EXISTS
    init_db()

    root = tk.Tk()
    root.title("AI Internship Diary Assistant")
    root.geometry("700x450")
    root.resizable(False, False)

    Dashboard(root, project_root=PROJECT_ROOT)
    root.mainloop()


if __name__ == "__main__":
    main()
