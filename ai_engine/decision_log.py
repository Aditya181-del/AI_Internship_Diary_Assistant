from datetime import datetime, date
from utils.config import INTERNSHIP_START_DATE, COMPANY_NAME


def build_decision_log(is_first_day: bool, input_mode: str) -> dict:
    """
    Builds an explainability log describing
    why and how the diary content was generated.
    """
    today = date.today()

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "generation_date": today.isoformat(),
        "internship_start_date": INTERNSHIP_START_DATE.isoformat(),
        "day_type": "FIRST_DAY" if is_first_day else "ROUTINE_DAY",
        "input_mode": input_mode,  # "text" or "voice"
        "company_name": COMPANY_NAME,
        "company_mention_policy": (
            "Mandatory on first day, contextual on routine days"
        ),
        "work_summary_rules": {
            "tone": "Formal academic",
            "person": "First person",
            "word_limit": "80–120",
            "content": "Tasks and exposure only",
        },
        "learning_outcome_rules": {
            "tone": "Formal academic",
            "person": "First person",
            "word_limit": "50–80",
            "content": "Skills and understanding only",
        },
        "ai_model": "mistral (ollama, local)",
        "human_in_the_loop": {
            "auto_fill_approved": True,
            "manual_submission_required": True,
        },
    }
