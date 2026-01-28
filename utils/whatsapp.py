from twilio.rest import Client
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_WHATSAPP = os.getenv("TWILIO_WHATSAPP_FROM")
TO_WHATSAPP = os.getenv("TWILIO_WHATSAPP_TO")


def send_whatsapp_reminder():
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    today = date.today().strftime("%d %b %Y")

    message = client.messages.create(
        from_=FROM_WHATSAPP,
        to=TO_WHATSAPP,
        body=(
            f"📘 VTU Internship Diary Reminder\n\n"
            f"Your internship diary for *{today}* is not yet filled.\n\n"
            f"Please complete it today to stay compliant with VTU guidelines."
        ),
    )

    return message.sid
