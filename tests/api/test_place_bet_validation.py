import allure
import pytest

from betting_flow_e2e.api.assertions import assert_error_response
from betting_flow_e2e.api.client import ApiClient, BalanceState
from betting_flow_e2e.domain.matches import match_label


@pytest.mark.critical
@pytest.mark.negative
@pytest.mark.regression
@pytest.mark.api
@allure.epic("Betting flow")
@allure.feature("Place bet API")
@allure.story("Reject stake above maximum at the service boundary")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("api", "regression", "negative", "critical")
def test_api_rejects_stake_above_maximum(
    api_client: ApiClient,
    clean_balance: BalanceState,
) -> None:
    """
    Chosen as the API validation/business-rule test because max-stake enforcement is a
    critical backend financial guardrail that must hold even when frontend validation is bypassed.
    """
    with allure.step("Load the first upcoming match"):
        match = api_client.get_first_upcoming_match()
        allure.dynamic.parameter("match", match_label(match))

    with allure.step("Submit a stake above the configured maximum"):
        response = api_client.post_place_bet_raw(
            {
                "matchId": match["id"],
                "selection": "HOME",
                "stake": 100.01,
            }
        )
        allure.attach(
            response.text,
            name="Place bet rejection response",
            attachment_type=allure.attachment_type.JSON,
        )

    with allure.step("Verify validation error and unchanged balance"):
        assert_error_response(
            response,
            expected_status=422,
            expected_error="invalid_stake_max",
            expected_message_fragment="100.00",
        )
        balance_after_rejection = api_client.get_balance_state()
        assert balance_after_rejection == clean_balance, (
            f"Rejected bet changed balance: before={clean_balance}, after={balance_after_rejection}"
        )
