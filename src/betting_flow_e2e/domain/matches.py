from datetime import date
from typing import Any

type MatchData = dict[str, Any]


def first_upcoming_match(matches: list[MatchData], today: date | None = None) -> MatchData:
    if not matches:
        raise ValueError("No matches returned by the application.")

    current_day = (today or date.today()).isoformat()
    return next(
        (match for match in matches if match["kickoffDate"] >= current_day),
        matches[0],
    )


def match_label(match: MatchData) -> str:
    return f"{match['homeTeam']} vs {match['awayTeam']}"
