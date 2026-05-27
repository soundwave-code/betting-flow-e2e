from decimal import Decimal
from typing import Self

from selenium.webdriver.common.by import By

from betting_flow_e2e.ui.base_page import BasePage
from betting_flow_e2e.ui.selectors import test_id
from betting_flow_e2e.utils.money import parse_eur


class ReceiptModal(BasePage):
    MODAL = test_id("modal-success", (By.ID, "modal-success"))
    BET_ID = test_id("modal-success-bet-id", (By.ID, "modal-success-bet-id"))
    MATCH = test_id("modal-success-match", (By.ID, "modal-success-match"))
    STAKE = test_id("modal-success-stake", (By.ID, "modal-success-stake"))
    ODDS = test_id("modal-success-odds", (By.ID, "modal-success-odds"))
    PAYOUT = test_id("modal-success-payout", (By.ID, "modal-success-payout"))
    PLACED_AT = test_id("modal-success-placed-at", (By.ID, "modal-success-placed-at"))
    CLOSE = test_id("modal-success-close", (By.ID, "modal-success-close"))

    def wait_open(self) -> Self:
        self.visible(self.MODAL)
        return self

    def bet_id(self) -> str:
        return self.text_of(self.BET_ID)

    def match(self) -> str:
        return self.text_of(self.MATCH)

    def stake(self) -> Decimal:
        return parse_eur(self.text_of(self.STAKE))

    def odds(self) -> Decimal:
        return Decimal(self.text_of(self.ODDS))

    def payout(self) -> Decimal:
        return parse_eur(self.text_of(self.PAYOUT))

    def placed_at(self) -> str:
        return self.text_of(self.PLACED_AT)

    def close(self) -> None:
        self.click(self.CLOSE)
        self.wait_until_hidden(self.MODAL)
