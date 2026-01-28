from datetime import date
from utils.db import get_connection
from utils.date_utils import get_working_days


def get_filled_dates():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT date FROM diary_entries")
    rows = cursor.fetchall()

    conn.close()

    return {row[0] for row in rows}


def get_missed_days(today=None):
    if today is None:
        today = date.today()

    working_days = get_working_days()
    filled_dates = get_filled_dates()

    missed = []

    for d in working_days:
        if d < today and d.isoformat() not in filled_dates:
            missed.append(d)

    return missed
