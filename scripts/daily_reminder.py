import sys
import os
from datetime import date
from dotenv import load_dotenv

# -------------------------------------------------
# 🔧 Fix Python path
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from utils.reminder import should_remind_today
from utils.whatsapp import send_whatsapp_reminder

# -------------------------------------------------
# 🔐 Load env
# -------------------------------------------------
load_dotenv()


def send_email_notification():
    import smtplib
    from email.message import EmailMessage

    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

    msg = EmailMessage()
    msg["Subject"] = "VTU Internship Diary Reminder"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    msg.set_content(
        f"""
Hello,

This is a reminder that your VTU internship diary for today
({date.today()}) has not been filled.

Please complete it before the day ends.

Regards,
AI Internship Diary Assistant
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)


# -------------------------------------------------
# 🚀 ENTRY
# -------------------------------------------------
if __name__ == "__main__":
    today = date.today()

    if should_remind_today(today):
        print(f"🔔 Reminder triggered for {today}")

        # Email
        send_email_notification()
        print("📧 Email reminder sent")

        # WhatsApp
        sid = send_whatsapp_reminder()
        print(f"📱 WhatsApp reminder sent (SID: {sid})")

    else:
        print(f"[OK] Diary already filled or non-working day ({today})")


# -------------------------------------------------
# 🚀 ENTRY POINT
# -------------------------------------------------
if __name__ == "__main__":
    today = date.today()

    if should_remind_today(today):
        print(f"[EMAIL REMINDER] Diary not filled for {today}")
        send_email_notification()
        print("📧 Email reminder sent.")
    else:
        print(f"[OK] Diary already filled or non-working day ({today})")


'''
import sys
import os
from datetime import date
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# -------------------------------------------------
# 🔧 Fix Python path
# -------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# -------------------------------------------------
# 🔐 Load environment variables
# -------------------------------------------------
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECEIVER:
    raise RuntimeError("❌ Email credentials missing in .env file")

# -------------------------------------------------
# 🔔 Desktop notification (Windows)
# -------------------------------------------------
try:
    from win10toast import ToastNotifier

    notifier = ToastNotifier()
except ImportError:
    notifier = None


def send_desktop_notification():
    if notifier:
        notifier.show_toast(
            "VTU Internship Reminder (TEST)",
            "⚠️ TEST: Internship diary reminder triggered.",
            duration=10,
            threaded=True,
        )


def send_email_notification():
    msg = EmailMessage()
    msg["Subject"] = "TEST: VTU Internship Diary Reminder"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    msg.set_content(
        f"""
Hello,

This is a TEST reminder.

If you are reading this email, your email reminder system
for the VTU Internship Diary Assistant is working correctly.

Date: {date.today()}

You can now safely enable the real reminder logic.

Regards,
AI Internship Diary Assistant (Test Mode)
"""
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)


# -------------------------------------------------
# 🚀 ENTRY POINT — TEST MODE (FORCED REMINDER)
# -------------------------------------------------
if __name__ == "__main__":
    print("🧪 TEST MODE: Forcing reminder...")

    send_desktop_notification()
    send_email_notification()

    print("✅ Desktop notification sent")
    print("📧 Test email sent successfully")
'''
