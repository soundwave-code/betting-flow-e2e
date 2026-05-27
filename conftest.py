import warnings
from collections.abc import Generator, Iterator
from pathlib import Path

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from betting_flow_e2e.api.client import ApiClient, BalanceState
from betting_flow_e2e.config import Settings, SettingsOverrides, load_settings
from betting_flow_e2e.reporting.artifacts import capture_browser_artifacts
from betting_flow_e2e.ui.driver_factory import create_driver


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("betting-flow-e2e")
    group.addoption("--base-url", default=None, help="Application base URL.")
    group.addoption("--user-id", default=None, help="Override the assignment test user ID.")
    group.addoption(
        "--browser",
        choices=("chrome",),
        default=None,
        help="Browser under test. Currently supports Chrome.",
    )
    group.addoption(
        "--headless",
        action="store_true",
        dest="headless",
        default=None,
        help="Run the browser without a visible window.",
    )
    group.addoption(
        "--headed",
        action="store_false",
        dest="headless",
        default=None,
        help="Run the browser with a visible window.",
    )
    group.addoption("--timeout", type=float, default=None, help="Default wait/API timeout.")
    group.addoption(
        "--window-size",
        default=None,
        help="Browser window size in WIDTHxHEIGHT format, for example 1440x1000.",
    )
    group.addoption("--remote-url", default=None, help="Remote WebDriver URL.")
    group.addoption(
        "--artifacts-dir",
        action="store",
        default="artifacts",
        help="Directory for Selenium failure artifacts.",
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


def _should_capture_browser_artifacts(report: pytest.TestReport | None) -> bool:
    return bool(report and (report.failed or getattr(report, "wasxfail", None)))


@pytest.fixture(scope="session")
def settings(pytestconfig: pytest.Config) -> Settings:
    return load_settings(
        SettingsOverrides(
            base_url=pytestconfig.getoption("--base-url"),
            user_id=pytestconfig.getoption("--user-id"),
            timeout_seconds=pytestconfig.getoption("--timeout"),
            headless=pytestconfig.getoption("headless"),
            browser=pytestconfig.getoption("--browser"),
            window_size=pytestconfig.getoption("--window-size"),
            remote_webdriver_url=pytestconfig.getoption("--remote-url"),
        )
    )


@pytest.fixture
def api_client(settings: Settings) -> ApiClient:
    return ApiClient(
        base_url=settings.base_url,
        user_id=settings.user_id,
        timeout_seconds=settings.timeout_seconds,
    )


@pytest.fixture
def clean_balance(api_client: ApiClient) -> Iterator[BalanceState]:
    balance = api_client.reset_balance_state()
    try:
        yield balance
    finally:
        try:
            api_client.reset_balance_state()
        except Exception as error:
            warnings.warn(
                f"Failed to reset balance during teardown: {error}",
                RuntimeWarning,
                stacklevel=1,
            )


@pytest.fixture
def driver(request: pytest.FixtureRequest, settings: Settings) -> Generator[WebDriver, None, None]:
    browser = create_driver(settings)
    try:
        yield browser
    finally:
        try:
            report = getattr(request.node, "rep_call", None)
            if _should_capture_browser_artifacts(report):
                artifacts_dir = Path(request.config.getoption("--artifacts-dir"))
                capture_browser_artifacts(browser, artifacts_dir, request.node.nodeid)
        except Exception as error:
            print(f"Failed to capture browser artifacts: {error}")
        finally:
            browser.quit()
