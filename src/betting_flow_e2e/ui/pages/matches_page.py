from decimal import Decimal
from typing import Self

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from betting_flow_e2e.config import Settings
from betting_flow_e2e.ui.base_page import BasePage
from betting_flow_e2e.ui.selectors import test_id
from betting_flow_e2e.utils.money import parse_eur


class MatchesPage(BasePage):
    MATCH_LIST = test_id("match-list", (By.ID, "match-list"))
    MATCH_LIST_LOADING = test_id("match-list-loading", (By.ID, "match-list-loading"))
    HEADER_BALANCE = test_id("header-balance", (By.ID, "header-balance"))

    def __init__(self, driver: WebDriver, settings: Settings) -> None:
        super().__init__(driver, settings.timeout_seconds)
        self.settings = settings

    def open(self) -> Self:
        self.driver.get(self.settings.app_url)
        return self

    def wait_loaded(self) -> Self:
        self.wait_until_hidden(self.MATCH_LIST_LOADING)
        self.visible(self.MATCH_LIST)
        return self

    def header_balance(self) -> Decimal:
        return parse_eur(self.text_of(self.HEADER_BALANCE))

    def select_outcome(self, match_id: str, selection: str) -> None:
        button_id = f"odds-{match_id}-{selection.lower()}"
        self.click(test_id(button_id, (By.ID, button_id)))
