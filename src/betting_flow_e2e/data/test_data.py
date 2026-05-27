from dataclasses import dataclass
from decimal import Decimal

from betting_flow_e2e.domain.betting import Selection


@dataclass(frozen=True, slots=True)
class SingleBetData:
    selection: Selection
    stake: Decimal


SUCCESSFUL_SINGLE_BET = SingleBetData(
    selection="HOME",
    stake=Decimal("10.00"),
)
