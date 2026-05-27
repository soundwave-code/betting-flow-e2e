# Execution Results

## Run Context

| Field | Value |
|---|---|
| Execution date | 2026-05-27 |
| Application | `https://qae-assignment-tau.vercel.app` |
| Test user | `candidate-oKClvQ200G` |
| Related documents | [Test Plan](test_plan.md), [Bug Reports](bug_reports.md) |


## Test Plan Execution Summary

| Test Case | Result | Evidence / Defects |
|---|---|---|
| [TC-001](test_plan.md#tc-001): Match List Display | Fail | Past matches are displayed and kickoff time data is incomplete. See [BUG-001](bug_reports.md#bug-001), [BUG-002](bug_reports.md#bug-002), [BUG-003](bug_reports.md#bug-003). |
| [TC-002](test_plan.md#tc-002): Place a Valid Single Bet | Fail / expected automation xfail | Bet placement succeeds, but receipt and balance consistency fail. See [BUG-004](bug_reports.md#bug-004), [BUG-005](bug_reports.md#bug-005), [BUG-006](bug_reports.md#bug-006), [BUG-011](bug_reports.md#bug-011). Automation observed that the header balance remains unchanged after an accepted bet until page refresh. |
| [TC-003](test_plan.md#tc-003): Validate Stake and Invalid Stake Formats | Partial pass | API maximum-stake rejection passed: `stake: 100.01` returned `422 invalid_stake_max`. Full UI stake-format matrix was not automated in this scoped submission. |
| [TC-004](test_plan.md#tc-004): Date and Odds Filters | Fail / partial execution | Odds filter range does not match documented boundaries. See [BUG-008](bug_reports.md#bug-008). Full date-filter matrix was not automated in this scoped submission. |
| [TC-005](test_plan.md#tc-005): API Contract and Validation for Betting Flow | Mixed | Core contracts and validation checks mostly pass, but API currency, reset persistence, and malformed JSON handling fail. See [BUG-007](bug_reports.md#bug-007), [BUG-009](bug_reports.md#bug-009), [BUG-010](bug_reports.md#bug-010). |

## API Execution Results


| # | Check | Expected Result | Actual Result | Status |
|---:|---|---|---|---|
| 1 | `GET /api/matches` | Response returns `200`; match list contains required fields: `id`, `competition`, `kickoffDate`, `homeTeam`, `awayTeam`, and numeric odds values for `home`, `draw`, and `away`. | Response returned `HTTP 200`; `103` matches returned; required fields and numeric odds were present. | Pass |
| 2 | `GET /api/balance` | Response returns `200`; response contains `balance` as a number and `currency: EUR`. | Response returned `HTTP 200`; body contained `balance: 120` and `currency: EUR`. | Pass |
| 3 | Valid `POST /api/place-bet` | Response returns `200`; bet is created; response contains `message`, `matchId`, `selection`, `stake`, `odds`, `payout`, `balance`, and `currency: EUR`. | Bet was created successfully and required fields were present, but response returned `currency: USD`. | Fail |
| 4 | Response values match submitted request | Response `matchId`, `selection`, and `stake` match submitted values. | Response returned `matchId: premier-league-manutd-chelsea`, `selection: HOME`, and `stake: 10`. | Pass |
| 5 | Payout calculation | `payout = stake x odds`. | For stake `10` and odds `2.45`, expected payout was `24.50`; response returned `24.5`. | Pass |
| 6 | Persisted balance after successful bet | Following `GET /api/balance` returns the same balance as `POST /api/place-bet`. | `POST /api/place-bet` returned `balance: 110`; following `GET /api/balance` also returned `balance: 110`. | Pass |
| 7 | Currency consistency after successful bet | API responses should use `currency: EUR`. | `POST /api/place-bet` returned `currency: USD`, while `GET /api/balance` returned `currency: EUR`. | Fail |
| 8 | `POST /api/reset-balance` contract | Response returns `200`; response contains `message`, `balance`, and `currency: EUR`. | Response returned `HTTP 200`; body contained `message: Balance reset successfully`, `balance: 125.5`, and `currency: EUR`. | Pass |
| 9 | Persisted balance after reset | Following `GET /api/balance` should return the same balance as the reset response. | `POST /api/reset-balance` returned `balance: 125.5`, but following `GET /api/balance` returned `balance: 120`. | Fail |
| 10 | Invalid stake above maximum | Stake above `100.00` should be rejected with `422`. | Request with `stake: 100.01` returned `HTTP 422` and `error: invalid_stake_max`. | Pass |
| 11 | Missing `x-user-id` | Request without `x-user-id` should be rejected with `401`. | Request returned `HTTP 401` and `error: missing_user_id`. | Pass |
| 12 | Invalid selection | Invalid selection should be rejected with `422`. | Request with `selection: INVALID` returned `HTTP 422` and `error: invalid_selection`. | Pass |
| 13 | Malformed JSON payload | Malformed request payload should be rejected with `400`. | Malformed JSON returned `HTTP 500` and `error: internal_server_error`. | Fail |
| 14 | Extra unsupported field | A valid request with an extra unsupported field should not fail because of that field; payout and balance should remain consistent. | Request succeeded; payout and persisted balance were consistent, but response still returned `currency: USD`. | Pass with known currency issue |

## Defect Summary

| Bug | Area | Severity | Execution Impact |
|---|---|---|---|
| [BUG-001](bug_reports.md#bug-001) | Match list | Critical | Fails TC-001 event eligibility expectation. |
| [BUG-002](bug_reports.md#bug-002) | Match list | Medium | Fails TC-001 kickoff metadata expectation. |
| [BUG-003](bug_reports.md#bug-003) | Match list | Low | Fails TC-001 full kickoff date/time expectation for one upcoming match. |
| [BUG-004](bug_reports.md#bug-004) | Receipt | Critical | Fails TC-002 payout consistency. |
| [BUG-005](bug_reports.md#bug-005) | Receipt | High | Fails TC-002 match-order consistency. |
| [BUG-006](bug_reports.md#bug-006) | Receipt | High | Fails TC-002 receipt completeness because selected outcome is missing. |
| [BUG-007](bug_reports.md#bug-007) | API | Medium | Fails TC-005 currency consistency for successful placement. |
| [BUG-008](bug_reports.md#bug-008) | Filters | Low | Fails TC-004 documented odds-range expectation. |
| [BUG-009](bug_reports.md#bug-009) | API | High | Fails TC-005 reset persistence consistency. |
| [BUG-010](bug_reports.md#bug-010) | API | Medium | Fails TC-005 malformed-payload error-class expectation. |
| [BUG-011](bug_reports.md#bug-011) | UI balance | High | Fails TC-002 immediate post-bet balance update; balance updates after page refresh. |
