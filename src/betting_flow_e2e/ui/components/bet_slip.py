from decimal import Decimal
from typing import Self

from selenium.webdriver.common.by import By

from betting_flow_e2e.ui.base_page import BasePage
from betting_flow_e2e.ui.selectors import test_id
from betting_flow_e2e.utils.money import parse_eur


class BetSlip(BasePage):
    COUNT = test_id("bet-slip-count", (By.ID, "bet-slip-count"))
    STAKE_INPUT = test_id("bet-slip-stake-input", (By.ID, "bet-slip-stake-input"))
    TOTAL_STAKE = test_id("bet-slip-total-stake", (By.ID, "bet-slip-total-stake"))
    POTENTIAL_PAYOUT = test_id(
        "bet-slip-potential-payout",
        (By.ID, "bet-slip-potential-payout"),
    )
    PLACE_BET = test_id("bet-slip-place-bet", (By.ID, "bet-slip-place-bet"))
    SELECTION_CARD = test_id("bet-selection-card", (By.CSS_SELECTOR, ".betSelectionCard"))

    def wait_for_selection(self) -> Self:
        self.visible(self.SELECTION_CARD)
        return self

    def selection_text(self) -> str:
        return self.text_of(self.SELECTION_CARD)

    def enter_stake(self, value: str) -> None:
        field = self.visible(self.STAKE_INPUT)
        field.clear()
        field.send_keys(value)

    def total_stake(self) -> Decimal:
        return parse_eur(self.text_of(self.TOTAL_STAKE))

    def potential_payout(self) -> Decimal:
        return parse_eur(self.text_of(self.POTENTIAL_PAYOUT))

    def place_bet(self) -> None:
        self.click(self.PLACE_BET)

    def wait_empty(self) -> None:
        self.wait.until(lambda _: self.text_of(self.COUNT) == "0")
