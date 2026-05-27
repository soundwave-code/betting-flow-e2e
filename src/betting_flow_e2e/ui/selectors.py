"""Selector targets that prefer stable test IDs and keep narrow live-app fallbacks."""

from dataclasses import dataclass

from selenium.webdriver.common.by import By

type Locator = tuple[str, str]


@dataclass(frozen=True, slots=True)
class UiTarget:
    test_id: str
    fallback: Locator | None = None

    @property
    def locators(self) -> tuple[Locator, ...]:
        preferred = (By.CSS_SELECTOR, f'[data-testid="{self.test_id}"]')
        if self.fallback is None:
            return (preferred,)
        return (preferred, self.fallback)


def test_id(value: str, fallback: Locator | None = None) -> UiTarget:
    return UiTarget(test_id=value, fallback=fallback)


type Target = Locator | UiTarget
