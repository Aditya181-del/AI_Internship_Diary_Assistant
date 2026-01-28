import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import sys
import os
import json

from utils.progress import get_progress

BG_COLOR = "#121212"
CARD_COLOR = "#1e1e1e"
PRIMARY = "#4fc3f7"
TEXT_PRIMARY = "#eaeaea"
TEXT_SECONDARY = "#b0b0b0"
SUCCESS = "#81c784"


class Dashboard:
    def __init__(self, root, project_root):
        self.root = root
        self.project_root = project_root
        self.root.configure(bg=BG_COLOR)

        self.status_var = tk.StringVar(value="Ready.")
        self.build_ui()
        self.animate_progress()

    # ---------------- UI ----------------

    def build_ui(self):
        container = tk.Frame(self.root, bg=BG_COLOR)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            container,
            text="AI Internship Diary Assistant",
            font=("Segoe UI", 18, "bold"),
            bg=BG_COLOR,
            fg=PRIMARY,
        ).pack(pady=10)

        completed, total, percent = get_progress()

        tk.Label(
            container,
            text=(
                f"Completed Days: {completed}\n"
                f"Total Days: {total}\n"
                f"Completion: {percent:.2f} %"
            ),
            bg=BG_COLOR,
            fg=TEXT_PRIMARY,
            justify="left",
        ).pack()

        self.progress_value = tk.DoubleVar(value=0)
        ttk.Progressbar(
            container,
            variable=self.progress_value,
            length=420,
        ).pack(pady=10)

        self.progress_label = tk.Label(
            container,
            fg=TEXT_SECONDARY,
            bg=BG_COLOR,
        )
        self.progress_label.pack()

        tk.Button(
            container,
            text="🧠 Fill Diary (Text Notes)",
            width=34,
            command=self.run_text_flow,
        ).pack(pady=6)

        tk.Button(
            container,
            text="🧠 View Decision Log",
            width=34,
            command=self.show_decision_log,
        ).pack(pady=6)

        tk.Button(
            container,
            text="✅ I have submitted the diary",
            width=34,
            command=self.mark_done,
        ).pack(pady=15)

        tk.Label(
            container,
            textvariable=self.status_var,
            fg=SUCCESS,
            bg=BG_COLOR,
            wraplength=500,
            justify="center",
        ).pack()

    # ---------------- PROGRESS ----------------

    def animate_progress(self):
        _, _, percent = get_progress()
        target = int(round(percent))
        current = 0

        def step():
            nonlocal current
            if current <= target:
                self.progress_value.set(current)
                self.progress_label.config(text=f"{percent:.2f} %")
                current += 1
                self.root.after(15, step)

        step()

    # ---------------- FLOW ----------------

    def run_text_flow(self):
        notes = simpledialog.askstring(
            "Diary Notes",
            "Enter short notes for today's work:",
            parent=self.root,
        )
        if not notes:
            return

        self.launch_bot(notes)

    def launch_bot(self, notes: str):
        automation_dir = os.path.join(self.project_root, "automation")
        os.makedirs(automation_dir, exist_ok=True)

        # Clean flags
        for f in (
            "PORTAL_READY.flag",
            "APPROVAL_OK.flag",
            "USER_DONE.flag",
        ):
            path = os.path.join(automation_dir, f)
            if os.path.exists(path):
                os.remove(path)

        with open(
            os.path.join(automation_dir, "NOTES.txt"), "w", encoding="utf-8"
        ) as f:
            f.write(notes)

        with open(os.path.join(automation_dir, "INPUT_MODE.flag"), "w") as f:
            f.write("text")

        self.status_var.set("Launching VTU InternYet portal…")

        subprocess.Popen(
            [sys.executable, "automation/portal_bot.py"],
            cwd=self.project_root,
        )

        self.root.after(500, self.wait_for_portal_ready)

    def wait_for_portal_ready(self):
        ready_flag = os.path.join(self.project_root, "automation", "PORTAL_READY.flag")

        if not os.path.exists(ready_flag):
            self.root.after(500, self.wait_for_portal_ready)
            return

        approve = messagebox.askyesno(
            "Confirm Auto-Fill",
            "Date is confirmed in VTU InternYet.\n\n"
            "Do you want the AI to auto-fill the diary now?\n\n"
            "You will review and submit manually.",
            parent=self.root,
        )

        if approve:
            with open(
                os.path.join(self.project_root, "automation", "APPROVAL_OK.flag"),
                "w",
            ) as f:
                f.write("OK")
            self.status_var.set("Auto-filling diary content…")
        else:
            self.status_var.set("Auto-fill cancelled.")

    # ---------------- DECISION LOG ----------------

    def show_decision_log(self):
        path = os.path.join(self.project_root, "automation", "LAST_DECISION_LOG.json")

        if not os.path.exists(path):
            messagebox.showinfo("Decision Log", "No decision log available.")
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        win = tk.Toplevel(self.root)
        win.title("AI Decision Log")
        win.geometry("600x500")

        text = tk.Text(win, wrap="word")
        text.insert("end", json.dumps(data, indent=2))
        text.config(state="disabled")
        text.pack(expand=True, fill="both")

    # ---------------- USER DONE ----------------

    def mark_done(self):
        with open(
            os.path.join(self.project_root, "automation", "USER_DONE.flag"),
            "w",
        ) as f:
            f.write("DONE")

        self.status_var.set("Submission confirmed. You may close the browser.")
