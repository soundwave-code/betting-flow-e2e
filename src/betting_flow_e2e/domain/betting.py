from decimal import Decimal
from typing import Literal

from betting_flow_e2e.utils.money import money

type Selection = Literal["HOME", "DRAW", "AWAY"]
type OddsKey = Literal["home", "draw", "away"]

ODDS_KEY_BY_SELECTION: dict[Selection, OddsKey] = {
    "HOME": "home",
    "DRAW": "draw",
    "AWAY": "away",
}


def odds_key_for(selection: Selection) -> OddsKey:
    return ODDS_KEY_BY_SELECTION[selection]


def payout(stake: Decimal, odds: Decimal) -> Decimal:
    return money(stake * odds)
