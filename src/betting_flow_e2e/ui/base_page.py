from collections.abc import Callable

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait

from betting_flow_e2e.ui.selectors import Locator, Target, UiTarget

type ElementPredicate = Callable[[WebElement], bool]


class BasePage:
    def __init__(self, driver: WebDriver, timeout_seconds: float = 10) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout_seconds)

    def visible(self, target: Target) -> WebElement:
        return self._find_first(target, lambda element: element.is_displayed())

    def clickable(self, target: Target) -> WebElement:
        return self._find_first(
            target,
            lambda element: element.is_displayed() and element.is_enabled(),
        )

    def click(self, target: Target) -> None:
        self.clickable(target).click()

    def text_of(self, target: Target) -> str:
        return self.visible(target).text

    def wait_until_hidden(self, target: Target) -> None:
        locators = self._locators(target)

        def all_hidden(driver: WebDriver) -> bool:
            for locator in locators:
                for element in driver.find_elements(*locator):
                    try:
                        if element.is_displayed():
                            return False
                    except StaleElementReferenceException:
                        continue
            return True

        self.wait.until(all_hidden)

    def _find_first(self, target: Target, predicate: ElementPredicate) -> WebElement:
        locators = self._locators(target)

        def matching_element(driver: WebDriver) -> WebElement | bool:
            for locator in locators:
                for element in driver.find_elements(*locator):
                    try:
                        if predicate(element):
                            return element
                    except StaleElementReferenceException:
                        continue
            return False

        message = f"Could not find matching UI target. {target=!r}, {locators=!r}"
        return self.wait.until(matching_element, message=message)

    def _locators(self, target: Target) -> tuple[Locator, ...]:
        if isinstance(target, UiTarget):
            return target.locators
        return (target,)
