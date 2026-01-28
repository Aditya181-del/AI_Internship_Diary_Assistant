from datetime import date
from utils.db import get_connection
from utils.date_utils import get_working_days


def _parse_date(raw: str) -> date | None:
    """
    Safely parse legacy date formats from DB.
    Supports:
    - YYYY-MM-DD
    - 'YYYY, M, D'
    """
    raw = raw.strip()

    # ✅ Proper ISO format
    if "-" in raw:
        try:
            return date.fromisoformat(raw)
        except ValueError:
            return None

    # 🧯 Legacy tuple-like format: '2026, 2, 6'
    try:
        parts = [int(p.strip()) for p in raw.split(",")]
        if len(parts) == 3:
            return date(parts[0], parts[1], parts[2])
    except Exception:
        return None

    return None


def get_completed_dates():
    """
    Returns valid completed diary dates.
    Ignores malformed legacy rows safely.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT date FROM diary_entries")
    rows = cursor.fetchall()
    conn.close()

    dates = set()
    for (raw,) in rows:
        parsed = _parse_date(raw)
        if parsed:
            dates.add(parsed)

    return dates


def get_progress():
    """
    Returns:
    completed_days, total_days, percentage
    """
    working_days = set(get_working_days())
    completed_dates = get_completed_dates()

    completed = len(working_days & completed_dates)
    total = len(working_days)

    percent = (completed / total) * 100 if total else 0.0
    return completed, total, round(percent, 2)
