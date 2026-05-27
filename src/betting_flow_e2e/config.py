import os
from dataclasses import dataclass
from typing import Literal, cast
from urllib.parse import urlencode

type BrowserName = Literal["chrome"]

DEFAULT_USER_ID = "candidate-oKClvQ200G"


def _bool_env(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default

    normalized = raw.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean value: true/false, yes/no, on/off, or 1/0.")


def _int_env(name: str, default: int) -> int:
    return int(os.getenv(name, str(default)))


def _window_size(
    raw: str | None,
    default_width: int,
    default_height: int,
) -> tuple[int, int]:
    if raw is None:
        return default_width, default_height

    try:
        width, height = raw.lower().split("x", maxsplit=1)
        return int(width), int(height)
    except ValueError as error:
        raise ValueError(
            "Window size must use WIDTHxHEIGHT format, for example 1440x1000."
        ) from error


def _browser(raw: str) -> BrowserName:
    if raw != "chrome":
        raise ValueError(f"Unsupported BROWSER value: {raw}. Only chrome is supported.")
    return cast(BrowserName, raw)


@dataclass(frozen=True, slots=True, kw_only=True)
class Settings:
    base_url: str
    user_id: str
    timeout_seconds: float
    headless: bool
    browser: BrowserName
    browser_width: int
    browser_height: int
    remote_webdriver_url: str | None
    chrome_binary: str | None

    @property
    def app_url(self) -> str:
        return f"{self.base_url}/?{urlencode({'user-id': self.user_id})}"


@dataclass(frozen=True, slots=True, kw_only=True)
class SettingsOverrides:
    base_url: str | None = None
    user_id: str | None = None
    timeout_seconds: float | None = None
    headless: bool | None = None
    browser: BrowserName | None = None
    window_size: str | None = None
    remote_webdriver_url: str | None = None


def load_settings(overrides: SettingsOverrides | None = None) -> Settings:
    overrides = overrides or SettingsOverrides()

    default_width = _int_env("BROWSER_WIDTH", 1440)
    default_height = _int_env("BROWSER_HEIGHT", 1000)
    browser_width, browser_height = _window_size(
        overrides.window_size,
        default_width,
        default_height,
    )

    return Settings(
        base_url=(
            overrides.base_url or os.getenv("BASE_URL", "https://qae-assignment-tau.vercel.app")
        ).rstrip("/"),
        user_id=overrides.user_id or os.getenv("USER_ID", DEFAULT_USER_ID),
        timeout_seconds=(
            overrides.timeout_seconds
            if overrides.timeout_seconds is not None
            else float(os.getenv("TIMEOUT_SECONDS", "10"))
        ),
        headless=(
            overrides.headless if overrides.headless is not None else _bool_env("HEADLESS", True)
        ),
        browser=overrides.browser or _browser(os.getenv("BROWSER", "chrome")),
        browser_width=browser_width,
        browser_height=browser_height,
        remote_webdriver_url=(
            overrides.remote_webdriver_url
            if overrides.remote_webdriver_url is not None
            else os.getenv("REMOTE_WEBDRIVER_URL") or None
        ),
        chrome_binary=os.getenv("CHROME_BINARY") or None,
    )
