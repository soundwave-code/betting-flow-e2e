import json
import re
from pathlib import Path

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

try:
    import allure
except ModuleNotFoundError:
    allure = None

type LogEntries = list[dict[str, object]]


def safe_artifact_name(nodeid: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid).strip("_")


def capture_browser_artifacts(driver: WebDriver, artifacts_dir: Path, nodeid: str) -> None:
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    name = safe_artifact_name(nodeid)

    screenshot_path = artifacts_dir / f"{name}.png"
    page_source_path = artifacts_dir / f"{name}.html"
    current_url_path = artifacts_dir / f"{name}.url.txt"
    browser_log_path = artifacts_dir / f"{name}.browser.log.json"

    driver.save_screenshot(str(screenshot_path))
    page_source_path.write_text(driver.page_source, encoding="utf-8")
    current_url_path.write_text(driver.current_url, encoding="utf-8")
    _write_json(browser_log_path, _logs(driver, "browser"))

    _attach_to_allure(screenshot_path, "Browser screenshot", "PNG")
    _attach_to_allure(page_source_path, "Page source", "HTML")
    _attach_to_allure(current_url_path, "Current URL", "TEXT")
    _attach_to_allure(browser_log_path, "Browser console logs", "JSON")


def _write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _logs(driver: WebDriver, log_type: str) -> LogEntries:
    try:
        return driver.get_log(log_type)
    except WebDriverException:
        return []


def _attach_to_allure(path: Path, name: str, attachment_type_name: str) -> None:
    if allure is None:
        return

    attachment_type = getattr(allure.attachment_type, attachment_type_name)
    allure.attach.file(str(path), name=name, attachment_type=attachment_type)
