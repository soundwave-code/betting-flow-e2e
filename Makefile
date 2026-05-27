.PHONY: install check test api ui allure allure-open clean

PYTHON ?= python3
VENV_PYTHON := .venv/bin/python
TEST_USER_ID ?= candidate-oKClvQ200G
TEST_USER_ARG := --user-id $(TEST_USER_ID)
REPORT_ARGS := --artifacts-dir artifacts --html=reports/report.html --self-contained-html --junitxml=reports/junit.xml

install:
	$(PYTHON) -m venv .venv
	$(VENV_PYTHON) -m pip install -e ".[dev]"

check:
	$(VENV_PYTHON) -m ruff format --check .
	$(VENV_PYTHON) -m ruff check .
	$(VENV_PYTHON) -m compileall -q src tests conftest.py

test:
	$(VENV_PYTHON) -m pytest -q $(TEST_USER_ARG) $(REPORT_ARGS)

api:
	$(VENV_PYTHON) -m pytest tests/api -m api -q $(TEST_USER_ARG)

ui:
	$(VENV_PYTHON) -m pytest tests/ui -m "ui and smoke" --headless --artifacts-dir artifacts -q $(TEST_USER_ARG)

allure:
	$(VENV_PYTHON) -m pytest -q $(TEST_USER_ARG) --artifacts-dir artifacts --alluredir=reports/allure-results --clean-alluredir

allure-open:
	@command -v allure >/dev/null 2>&1 || { \
		echo "Allure CLI is not installed."; \
		echo "Install it with: brew install allure"; \
		echo "Then run: make allure-open"; \
		exit 1; \
	}
	allure serve reports/allure-results

clean:
	rm -rf .pytest_cache .ruff_cache artifacts reports src/*.egg-info
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
