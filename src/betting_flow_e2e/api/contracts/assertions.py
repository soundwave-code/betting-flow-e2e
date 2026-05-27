import json
from functools import cache
from importlib.resources import files
from typing import Any

import requests
from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

type JsonValue = Any
type JsonObject = dict[str, JsonValue]


@cache
def _openapi_spec() -> JsonObject:
    spec_path = files("betting_flow_e2e.api.contracts").joinpath("openapi.json")
    return json.loads(spec_path.read_text(encoding="utf-8"))


@cache
def _validator(schema_name: str) -> Draft202012Validator:
    spec = _openapi_spec()
    schema = {
        "$ref": f"#/components/schemas/{schema_name}",
        "components": spec["components"],
    }
    return Draft202012Validator(schema, format_checker=FormatChecker())


def _assert_schema(schema_name: str, payload: JsonValue) -> None:
    errors = sorted(_validator(schema_name).iter_errors(payload), key=_error_path)
    if errors:
        details = "\n".join(f"- {_format_error(error)}" for error in errors)
        raise AssertionError(f"{schema_name} contract mismatches:\n{details}")


def _error_path(error: ValidationError) -> str:
    return ".".join(str(part) for part in error.absolute_path)


def _format_error(error: ValidationError) -> str:
    path = _error_path(error) or "<response>"
    return f"{path}: {error.message}"


def assert_matches_contract(payload: JsonValue) -> None:
    _assert_schema("MatchesResponse", payload)


def assert_balance_contract(payload: JsonValue) -> None:
    _assert_schema("BalanceResponse", payload)


def assert_reset_balance_contract(payload: JsonValue) -> None:
    _assert_schema("ResetBalanceResponse", payload)


def _response_json(response: requests.Response) -> JsonValue:
    try:
        return response.json()
    except ValueError as error:
        raise AssertionError(
            "Expected JSON response but could not parse it. "
            f"HTTP {response.status_code}. Body: {response.text}"
        ) from error


def assert_place_bet_contract(response: requests.Response) -> None:
    payload = _response_json(response)
    schema_name = "PlaceBetSuccessResponse" if response.status_code == 200 else "ErrorResponse"
    _assert_schema(schema_name, payload)
