from utils.db import get_connection


def save_diary(date_str, notes, diary_text):
    conn = get_connection()
    cursor = conn.cursor()

    word_count = len(diary_text.split())

    cursor.execute(
        """
        INSERT OR REPLACE INTO diary_entries
        (date, notes, diary_text, word_count)
        VALUES (?, ?, ?, ?)
    """,
        (date_str, notes, diary_text, word_count),
    )

    conn.commit()
    conn.close()
