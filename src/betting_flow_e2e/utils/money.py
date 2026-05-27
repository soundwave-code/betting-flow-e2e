import re
from decimal import ROUND_HALF_UP, Decimal

type MoneyInput = Decimal | float | int | str


EUR_PATTERN: re.Pattern[str] = re.compile(r"-?\d+(?:\.\d{1,2})?")
CENT = Decimal("0.01")


def money(value: MoneyInput) -> Decimal:
    return Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP)


def parse_eur(text: str) -> Decimal:
    match = EUR_PATTERN.search(text.replace(",", "."))
    if not match:
        raise ValueError(f"No EUR amount found in text: {text!r}")
    return money(match.group(0))


def format_eur(value: MoneyInput) -> str:
    return f"€{money(value):.2f}"
