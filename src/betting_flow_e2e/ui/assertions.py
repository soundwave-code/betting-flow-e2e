from dataclasses import dataclass
from decimal import Decimal
from typing import Self

from betting_flow_e2e.domain.betting import Selection, odds_key_for
from betting_flow_e2e.domain.matches import MatchData, match_label
from betting_flow_e2e.ui.components.receipt_modal import ReceiptModal
from betting_flow_e2e.utils.money import money


@dataclass(frozen=True, slots=True)
class BetPlacementExpectation:
    match_id: str
    match_label: str
    selection: Selection
    stake: Decimal
    odds: Decimal
    initial_balance: Decimal
    bet_id_prefix: str = "#B-"

    @classmethod
    def from_match(
        cls,
        *,
        match: MatchData,
        selection: Selection,
        stake: Decimal,
        initial_balance: Decimal,
    ) -> Self:
        return cls(
            match_id=str(match["id"]),
            match_label=match_label(match),
            selection=selection,
            stake=stake,
            odds=money(match["odds"][odds_key_for(selection)]),
            initial_balance=initial_balance,
        )

    @property
    def payout(self) -> Decimal:
        return money(self.stake * self.odds)

    @property
    def expected_balance(self) -> Decimal:
        return money(self.initial_balance - self.stake)

    def report_parameters(self) -> dict[str, str]:
        return {
            "match": self.match_label,
            "selection": self.selection,
            "stake": str(self.stake),
            "odds": str(self.odds),
            "expected_payout": str(self.payout),
        }


@dataclass(frozen=True, slots=True)
class ReceiptSnapshot:
    bet_id: str
    match_label: str
    stake: Decimal
    odds: Decimal
    payout: Decimal
    placed_at: str

    @classmethod
    def from_modal(cls, receipt: ReceiptModal) -> Self:
        return cls(
            bet_id=receipt.bet_id(),
            match_label=receipt.match(),
            stake=receipt.stake(),
            odds=receipt.odds(),
            payout=receipt.payout(),
            placed_at=receipt.placed_at(),
        )

    @classmethod
    def capture_and_close(cls, receipt: ReceiptModal) -> Self:
        try:
            return cls.from_modal(receipt)
        finally:
            receipt.close()


def assert_placed_bet_state(
    *,
    receipt: ReceiptSnapshot,
    actual_balance: Decimal,
    expected: BetPlacementExpectation,
) -> None:
    mismatches = _receipt_mismatches(receipt, expected)
    if actual_balance != expected.expected_balance:
        mismatches.append(
            "header balance: expected before - stake; "
            f"before={expected.initial_balance}, "
            f"stake={expected.stake}, "
            f"expected_after={expected.expected_balance}, "
            f"actual_after={actual_balance}"
        )
    if mismatches:
        raise AssertionError("Placed bet UI mismatches:\n- " + "\n- ".join(mismatches))


def _receipt_mismatches(
    receipt: ReceiptSnapshot,
    expected: BetPlacementExpectation,
) -> list[str]:
    mismatches: list[str] = []

    if not receipt.bet_id.startswith(expected.bet_id_prefix):
        mismatches.append(
            f"bet id: expected prefix {expected.bet_id_prefix!r}, got {receipt.bet_id!r}"
        )
    if receipt.match_label != expected.match_label:
        mismatches.append(f"match: expected {expected.match_label!r}, got {receipt.match_label!r}")
    if receipt.stake != expected.stake:
        mismatches.append(f"stake: expected {expected.stake}, got {receipt.stake}")
    if receipt.odds != expected.odds:
        mismatches.append(f"odds: expected {expected.odds}, got {receipt.odds}")
    if receipt.payout != expected.payout:
        mismatches.append(f"payout: expected {expected.payout}, got {receipt.payout}")
    if not receipt.placed_at:
        mismatches.append("placed at: expected a non-empty timestamp")

    return mismatches
