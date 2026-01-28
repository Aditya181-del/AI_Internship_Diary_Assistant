from datetime import date
from utils.progress import get_completed_dates


INTERNSHIP_START_DATE = date(2026, 2, 2)  # confirmed start date


def get_day_mode(entry_date: date) -> str:
    """
    Determines whether the diary entry is for:
    - FIRST_DAY
    - ROUTINE_DAY
    """

    completed_dates = get_completed_dates()

    # First ever diary entry
    if not completed_dates:
        return "FIRST_DAY"

    # Explicit internship start date
    if entry_date == INTERNSHIP_START_DATE:
        return "FIRST_DAY"

    return "ROUTINE_DAY"
