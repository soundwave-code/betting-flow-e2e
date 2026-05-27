import allure
import pytest

from betting_flow_e2e.api.client import ApiClient, BalanceState
from betting_flow_e2e.config import Settings
from betting_flow_e2e.data.test_data import SUCCESSFUL_SINGLE_BET
from betting_flow_e2e.ui.assertions import (
    BetPlacementExpectation,
    ReceiptSnapshot,
    assert_placed_bet_state,
)
from betting_flow_e2e.ui.flows.betting_flow import BettingFlow


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.critical
@pytest.mark.known_bug(
    "BUG-004",
    reason="Success receipt payout does not match stake multiplied by odds.",
)
@pytest.mark.known_bug(
    "BUG-005",
    reason="Success receipt reverses match order.",
)
@pytest.mark.known_bug(
    "BUG-011",
    reason="Header balance is not reduced after an accepted bet until page refresh.",
)
@pytest.mark.xfail(
    reason=(
        "BUG-004/BUG-005/BUG-011: Success receipt shows an inconsistent payout, "
        "reverses match order, and header balance stays stale until refresh. "
        "Remove when the UI reflects the placed bet correctly."
    ),
    strict=True,
)
@allure.epic("Betting flow")
@allure.feature("Single bet placement")
@allure.story("User places one HOME selection and sees a receipt")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("ui", "smoke", "critical", "known_bug", "BUG-004", "BUG-005", "BUG-011")
def test_user_can_place_single_bet_and_see_consistent_receipt(
    driver,
    settings: Settings,
    api_client: ApiClient,
    clean_balance: BalanceState,
) -> None:
    """
    Chosen as the critical UI E2E because it exercises the customer-visible revenue path:
    match selection, bet slip calculation, successful placement, receipt consistency, and
    post-bet balance.
    """
    with allure.step("Load first upcoming match and expected bet values"):
        bet = SUCCESSFUL_SINGLE_BET
        expected_bet = BetPlacementExpectation.from_match(
            match=api_client.get_first_upcoming_match(),
            selection=bet.selection,
            stake=bet.stake,
            initial_balance=clean_balance.balance,
        )

        for name, value in expected_bet.report_parameters().items():
            allure.dynamic.parameter(name, value)

    with allure.step("Open matches page and verify starting balance"):
        flow = BettingFlow(driver, settings)
        matches_page = flow.open_matches()
        assert matches_page.header_balance() == expected_bet.initial_balance

    with allure.step("Select HOME outcome and verify bet slip selection"):
        bet_slip = flow.select_bet_on_open_page(
            matches_page,
            match_id=expected_bet.match_id,
            selection=expected_bet.selection,
        )
        assert expected_bet.match_label in bet_slip.selection_text()

    with allure.step("Enter stake and verify calculated potential payout"):
        bet_slip.enter_stake(f"{expected_bet.stake:.2f}")
        assert bet_slip.total_stake() == expected_bet.stake
        assert bet_slip.potential_payout() == expected_bet.payout

    with allure.step("Place bet and wait for success receipt"):
        receipt = flow.submit_selected_bet(bet_slip)

    with allure.step("Capture receipt details and close modal"):
        receipt_snapshot = ReceiptSnapshot.capture_and_close(receipt)

    with allure.step("Verify receipt, bet slip cleanup, and header balance after placement"):
        bet_slip.wait_empty()
        assert_placed_bet_state(
            receipt=receipt_snapshot,
            actual_balance=matches_page.header_balance(),
            expected=expected_bet,
        )
