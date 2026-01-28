import sqlite3
import pandas as pd
from pathlib import Path
from fpdf import FPDF

DB_PATH = Path("data/diary.db")
EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)


def fetch_all_entries():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT date, diary_text, word_count FROM diary_entries ORDER BY date", conn
    )
    conn.close()
    return df


def export_to_excel():
    df = fetch_all_entries()
    file_path = EXPORT_DIR / "internship_diary.xlsx"
    df.to_excel(file_path, index=False)
    return file_path


def export_to_pdf():
    df = fetch_all_entries()
    file_path = EXPORT_DIR / "internship_diary.pdf"

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for _, row in df.iterrows():
        pdf.add_page()
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Date: {row['date']}", ln=True)

        pdf.ln(5)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, row["diary_text"])

    pdf.output(str(file_path))
    return file_path
