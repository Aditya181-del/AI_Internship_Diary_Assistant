from datetime import date
from utils.progress import get_completed_dates
from utils.date_utils import is_working_day


def should_remind_today(today: date) -> bool:
    """
    Returns True if:
    - Today is a working day
    - AND today's diary entry is NOT filled
    """

    # 1️⃣ Not a working day → no reminder
    if not is_working_day(today):
        return False

    # 2️⃣ Check completed diary dates
    completed_dates = get_completed_dates()

    # 3️⃣ Already filled today → no reminder
    if today in completed_dates:
        return False

    # 4️⃣ Otherwise → remind
    return True
