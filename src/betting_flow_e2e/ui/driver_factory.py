from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

from betting_flow_e2e.config import Settings


def create_driver(settings: Settings) -> WebDriver:
    if settings.browser != "chrome":
        raise ValueError(f"Unsupported browser: {settings.browser}")

    options = ChromeOptions()
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={settings.browser_width},{settings.browser_height}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.set_capability(
        "goog:loggingPrefs",
        {"browser": "ALL"},
    )

    if settings.chrome_binary:
        options.binary_location = settings.chrome_binary

    if settings.remote_webdriver_url:
        driver = webdriver.Remote(command_executor=settings.remote_webdriver_url, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    driver.set_page_load_timeout(settings.timeout_seconds)
    return driver
