from typing import Any

import requests

from betting_flow_e2e.api.contracts.assertions import assert_place_bet_contract

type JsonObject = dict[str, Any]


def assert_error_response(
    response: requests.Response,
    *,
    expected_status: int,
    expected_error: str | None,
    expected_message_fragment: str | None,
) -> JsonObject:
    assert response.status_code == expected_status, (
        f"Expected HTTP {expected_status}, got {response.status_code}. Body: {response.text}"
    )
    assert_place_bet_contract(response)
    body = response.json()

    if expected_error is not None:
        assert body.get("error") == expected_error, body

    if expected_message_fragment is not None:
        actual_message = str(body.get("message", ""))
        assert expected_message_fragment.lower() in actual_message.lower(), body

    return body
