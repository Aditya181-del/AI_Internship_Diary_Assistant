from datetime import date, datetime
from ai_engine.diary_generator import generate_diary
from utils.db import init_db
from utils.diary_store import save_diary
from utils.progress import get_progress
from utils.missed_days import get_missed_days
from utils.voice_recorder import record_voice
from utils.speech_to_text import transcribe_audio
from utils.exporter import export_to_excel, export_to_pdf

init_db()

if __name__ == "__main__":
    today = date.today()

    missed = get_missed_days(today)
    if missed:
        print("\n⚠️ Missed Internship Days Detected:")
        for d in missed:
            print(f"- {d.isoformat()}")

    print("\nEnter the date you want to fill (YYYY-MM-DD)")
    print("Press Enter to fill today.")
    date_input = input("> ").strip()

    # ✅ Date validation
    if not date_input:
        entry_date = today.isoformat()
    else:
        try:
            entry_date = datetime.strptime(date_input, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("❌ Invalid date format. Please use YYYY-MM-DD.")
            exit()

    print("\nChoose input method:")
    print("1️⃣ Type notes")
    print("2️⃣ Speak (voice note)")
    choice = input("> ").strip()

    if choice == "2":
        audio_file = record_voice("data/voice_note.wav", duration=20)
        notes = transcribe_audio(audio_file)
        print("\n📝 Transcribed Notes:")
        print(notes)
    else:
        print("\nEnter your internship notes:")
        notes = input("> ")

    diary = generate_diary(notes)
    save_diary(entry_date, notes, diary)

    completed, total, percent = get_progress()

    print("\n--- Generated Internship Diary ---\n")
    print(diary)

    print("\n--- Internship Progress ---")
    print(f"Completed days: {completed}/{total}")
    print(f"Completion: {percent}%")

    print("\nDo you want to export your diary?")
    print("1️⃣ Excel")
    print("2️⃣ PDF")
    print("3️⃣ Both")
    print("Press Enter to skip.")
    export_choice = input("> ").strip()

    if export_choice == "1":
        path = export_to_excel()
        print(f"✅ Excel exported to {path}")
    elif export_choice == "2":
        path = export_to_pdf()
        print(f"✅ PDF exported to {path}")
    elif export_choice == "3":
        excel_path = export_to_excel()
        pdf_path = export_to_pdf()
        print(f"✅ Excel exported to {excel_path}")
        print(f"✅ PDF exported to {pdf_path}")
