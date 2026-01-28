from datetime import date, timedelta

# -------------------------------------------------
# 📅 Internship duration (FINAL)
# -------------------------------------------------
INTERNSHIP_START_DATE = date(2026, 2, 2)
INTERNSHIP_END_DATE = date(2026, 6, 1)


def is_working_day(d: date) -> bool:
    """
    Valid internship working day:
    - Within internship range
    - Monday to Friday
    """
    if d < INTERNSHIP_START_DATE or d > INTERNSHIP_END_DATE:
        return False
    return d.weekday() < 5


def get_working_days():
    """
    Returns all working days in internship duration.
    """
    days = []
    current = INTERNSHIP_START_DATE

    while current <= INTERNSHIP_END_DATE:
        if is_working_day(current):
            days.append(current)
        current += timedelta(days=1)

    return days
