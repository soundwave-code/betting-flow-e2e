from selenium.webdriver.remote.webdriver import WebDriver

from betting_flow_e2e.config import Settings
from betting_flow_e2e.domain.betting import Selection
from betting_flow_e2e.ui.components.bet_slip import BetSlip
from betting_flow_e2e.ui.components.receipt_modal import ReceiptModal
from betting_flow_e2e.ui.pages.matches_page import MatchesPage


class BettingFlow:
    def __init__(self, driver: WebDriver, settings: Settings) -> None:
        self.driver = driver
        self.settings = settings

    def open_matches(self) -> MatchesPage:
        return MatchesPage(self.driver, self.settings).open().wait_loaded()

    def select_bet_on_open_page(
        self,
        matches_page: MatchesPage,
        *,
        match_id: str,
        selection: Selection,
    ) -> BetSlip:
        matches_page.select_outcome(match_id, selection)
        return BetSlip(self.driver, self.settings.timeout_seconds).wait_for_selection()

    def submit_selected_bet(self, bet_slip: BetSlip) -> ReceiptModal:
        bet_slip.place_bet()
        return ReceiptModal(self.driver, self.settings.timeout_seconds).wait_open()
