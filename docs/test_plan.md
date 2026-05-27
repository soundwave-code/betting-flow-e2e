# Test Plan: Single Bet Placement

## Quick Navigation

| Test Case | Priority | Concise Description |
|---|---|---|
| [TC-001](#tc-001) | High | Match list displays eligible football events with required match details and odds. |
| [TC-002](#tc-002) | Critical | User places a valid single bet and checks slip, receipt, payout, and balance. |
| [TC-003](#tc-003) | Critical | Stake limits and invalid stake formats are rejected correctly. |
| [TC-004](#tc-004) | Medium | Date and odds filters show the correct subset of available matches. |
| [TC-005](#tc-005) | High | API contract and betting validation protect match, balance, and placement state. |

---

## Scope

This test plan covers the Single Bet Placement feature for the desktop web application.

The focus is on:
- football match list;
- single bet selection;
- successful bet placement;
- stake validation;
- payout and balance accuracy;
- receipt consistency;
- date and odds filters;
- API validation for critical business rules.

## Out of Scope

- Live betting
- Multi-bets / accumulators
- Other sports
- Mobile-specific UX

---

<a id="tc-001"></a>

## TC-001: Match List Display

**Priority:** High

**Risk Rationale:**  
The match list defines which events are available for betting. Incorrect event eligibility, missing match details, or wrong home/away display can lead to invalid selections, user confusion, and downstream issues in the bet slip and receipt.

**Preconditions:**
- User opens the desktop web application with a valid assignment user ID.

**Steps and Expected Results:**

| Step | Action | Expected Result |
|---:|---|---|
| 1 | Open the application and navigate to the match list. | Match list is displayed. |
| 2 | Review the sports/events shown in the list. | Only football/soccer matches are available in the match list. |
| 3 | Inspect team names on several match cards. | Each match displays two teams in home/away order. |
| 4 | Inspect competition and kickoff metadata on match cards. | Each match displays competition and kickoff date/time label. |
| 5 | Inspect available market buttons on match cards. | Each match displays three selectable odds buttons for home win, draw, and away win: `1`, `X`, `2`. |
| 6 | Review event status/date labels where available. | Matches available for betting are upcoming/pre-match events; past or live events are not available for betting. |

---

<a id="tc-002"></a>

## TC-002: Place a Valid Single Bet

**Priority:** Critical

**Risk Rationale:**  
This is the primary financial user journey of the product. If a valid bet cannot be placed, or if odds, stake, payout, receipt data, or balance are incorrect, the core betting functionality is broken and user funds may be affected. This scenario verifies that a valid single bet is placed successfully and that key financial values remain consistent between the match list, bet slip, receipt, and updated balance.

**Test Data:**

| Field | Value |
|---|---|
| Match | Any upcoming football match |
| Selection | Any valid outcome: `1`, `X`, or `2` |
| Stake | `10.00` |
| Currency | EUR (`€`) |

**Main Flow Steps and Expected Results:**

| Step | Action | Expected Result / Validation |
|---:|---|---|
| 1 | Open the betting page. | Bet slip is visible and fixed on the right side; header balance is displayed. |
| 2 | Select an odds button for an upcoming match, for example `1`, `X`, or `2`. | Selected outcome is added to the bet slip. |
| 3 | Record the current header balance, selected match, outcome, and odds value. | Values are available for receipt, payout, and balance comparison. |
| 4 | Enter a valid stake, for example `10.00`. | Stake is accepted; financial values use EUR (`€`); potential payout equals `stake x odds`. |
| 5 | Review the bet slip before placement. | Bet slip shows the selected match/outcome, entered stake, odds, total stake, and potential payout. |
| 6 | Click `Place Bet`. | Bet placement starts and the submit button shows a loading state, for example `Placing...`. |
| 7 | Wait until the placement resolves. | Bet placement completes without an error modal and the success receipt modal is displayed. |
| 8 | Review the receipt. | Receipt includes Bet ID, match details, selection, stake, odds at placement, potential payout, and placement timestamp. |
| 9 | Compare receipt values with the pre-placement values. | Receipt match, selection, stake, odds, and potential payout are consistent with the selected bet. |
| 10 | Close the receipt. | Receipt closes successfully and user returns to the main flow. |
| 11 | Check the updated balance. | Header/bet slip balance equals initial balance minus placed stake. |

**Expected Result Summary:**
- Bet slip is displayed as a fixed right-side panel.
- Selected outcome appears in the bet slip.
- Stake `10.00` is accepted.
- Potential payout is calculated as `stake x odds`.
- Stake, available balance, and potential payout are displayed in EUR (`€`) in the bet slip.
- Submit button enters loading state after clicking `Place Bet`.
- Bet placement resolves successfully.
- Success receipt modal is displayed.
- Receipt shows:
  - Bet ID;
  - match details;
  - selection;
  - stake;
  - odds at placement;
  - potential payout;
  - placement timestamp.
- Match, selection, stake, odds, and payout are consistent between the match list, bet slip, and receipt.
- Balance is reduced by the stake amount after successful placement.
- Updated balance is consistent in the header and bet slip.
- Closing the receipt returns the user to the main flow.

**Additional Check: Single-Bet Selection Behaviour**

| Action | Expected Result |
|---|---|
| Select odds for a different match while one selection is already active. | The new selection replaces the previous selection. |
| Review the bet slip after replacement. | Only one active selection is shown in the bet slip. |
| Use the per-selection remove `x`. | Current selection, stake, and potential payout are cleared. |
| Use `Remove All`. | Current selection, stake, and potential payout are cleared. |

**Additional Check: Failed Placement Handling**

If bet placement fails after clicking `Place Bet`, expected behaviour is:
- error modal is displayed with title `Something went wrong`;
- modal body explains that the bet could not be processed and suggests trying again;
- `Rebet` closes the modal and retries placement;
- `Close` and top-right `X` close the modal and clear the current selection/stake;
- balance remains unchanged;
- no success receipt is created.

---

<a id="tc-003"></a>

## TC-003: Validate Stake and Invalid Stake Formats

**Priority:** Critical

**Risk Rationale:**  
Stake validation protects user funds and business exposure. Incorrect validation can allow invalid financial values, incorrect payouts, or bets above the allowed limit.

**Preconditions:**
- User has selected an odds button for an upcoming match.

**Validation Matrix:**

| Case | Input / Action | Expected Result |
|---:|---|---|
| 1 | Try to place a bet with an empty stake. | Empty stake is rejected. |
| 2 | Enter invalid stake `0`. | Stake below minimum is rejected. |
| 3 | Enter invalid stake `0.99`. | Stake below minimum is rejected. |
| 4 | Enter valid min stake `1.00`. | Minimum valid stake is accepted according to the agreed specification. |
| 5 | Enter valid max stake `100.00`. | Stake `100.00` is accepted. |
| 6 | Enter stake `100.01`. | Stake above `100.00` is rejected. |
| 7 | Enter stake greater than the available balance. | Stake greater than available balance is rejected. |
| 8 | Enter non-numeric stake `abc`. | Non-numeric stake is rejected. |
| 9 | Enter negative stake `-10`. | Negative stake is rejected. |
| 10 | Enter stake with more than two decimals: `10.999`. | Stake with more than 2 decimal places is rejected. |
| 11 | Enter stake with more than one decimal separator: `10..50`. | Stake with more than one decimal separator is rejected. |
| 12 | Enter valid decimal format `10`. | Valid numeric value is accepted. |
| 13 | Enter valid decimal format `10.5`. | Valid numeric value with one decimal place is accepted. |
| 14 | Enter valid decimal format `10.50`. | Valid numeric value with two decimal places is accepted. |

**Expected Result Summary:**
- Stake input accepts valid numeric values with a single decimal separator and up to 2 decimal places.
- User sees clear validation messages:
  - `Minimum stake is €1.00`;
  - `Maximum stake is €100.00`;
  - `Insufficient balance`.
- Balance changes only after successful valid bet placement.

---

<a id="tc-004"></a>

## TC-004: Date and Odds Filters

**Priority:** Medium

**Risk Rationale:**  
Filters affect which betting options are visible to the user. Incorrect filtering may hide valid matches, show matches outside the selected date or odds range, or allow invalid odds ranges, which can lead to user confusion and poor bet selection.

**Steps and Expected Results:**

| Step | Action | Expected Result |
|---:|---|---|
| 1 | Open the date filter. | Date filter controls are available. |
| 2 | Select a single date, for example today or a future date. | Selected date is shown in the filter. |
| 3 | Apply the filter. | Match list refreshes. |
| 4 | Review the filtered match list. | Only matches for the selected date are displayed. |
| 5 | Reset the date filter. | Reset restores all matches. |
| 6 | Select a date range, for example from today to `D+2` in the future. | Date range is selected. |
| 7 | Apply the filter. | Match list refreshes. |
| 8 | Review the displayed results for the selected date range. | Only matches within the selected date range are displayed. |
| 9 | Reset the date filter. | Reset restores all matches. |
| 10 | Open the odds filter. | Odds filter controls are available. |
| 11 | Enter a valid min/max range, for example `1.01` to `1000.00`. | Valid odds range is accepted. |
| 12 | Apply the filter. | Match count updates and displayed odds are within the selected range. |
| 13 | Enter invalid odds below the minimum, for example `1.00`, and above the maximum, for example `1000.01`. | Invalid range values are identified. |
| 14 | Apply the filter. | Invalid range is rejected with clear feedback. |

**Expected Result Summary:**
- Date filter supports single day selection, today or in the future.
- Date filter supports a date range from today to `D+2` in the future.
- Reset restores all matches.
- Match count updates after filtering.
- Odds filter supports a min/max range.
- Invalid odds range is rejected with clear feedback.

---

<a id="tc-005"></a>

## TC-005: API Contract and Validation for Betting Flow

**Priority:** High

**Risk Rationale:**  
API validation protects the betting flow from invalid, unauthorised, or inconsistent requests. If API endpoints return incorrect match, balance, placement, or reset data, the UI may display invalid betting options, create invalid bets, or show an incorrect user balance.

**API Contract Checks:**

| Step | Action | Expected Result / Validation |
|---:|---|---|
| 1 | Send `GET /api/matches` with a valid `x-user-id` header. | Request is accepted. |
| 2 | Inspect the matches response status. | Status is `200`. |
| 3 | Inspect each match object. | Each match contains `id`, `competition`, `kickoffDate`, `homeTeam`, `awayTeam`, and `odds`; `id` is a non-empty string; `competition` is a string; `kickoffDate` is a `YYYY-MM-DD` string; `homeTeam` and `awayTeam` are strings; `odds` contains numeric `home`, `draw`, and `away` values. |
| 4 | Send `GET /api/balance` with a valid `x-user-id` header. | Request is accepted. |
| 5 | Inspect the balance response status. | Status is `200`. |
| 6 | Inspect the balance response body. | Response contains numeric `balance` and `currency` equal to `EUR`. |

**Valid Placement and Reset Checks:**

| Step | Action | Expected Result / Validation |
|---:|---|---|
| 7 | Send a valid `POST /api/place-bet` with a valid `x-user-id`, valid `matchId` from `GET /api/matches`, valid `selection` (`HOME`, `DRAW`, or `AWAY`), and valid `stake`, for example `10.00`. | Request is accepted. |
| 8 | Inspect the place-bet response status. | Status is `200`. |
| 9 | Inspect the place-bet response body. | Response contains `message`, `matchId`, `selection`, `stake`, `odds`, `payout`, `balance`, and `currency: EUR`. |
| 10 | Compare response values with the submitted request. | Response `matchId`, `selection`, and `stake` match the submitted values. |
| 11 | Calculate expected payout from the response values. | `payout = stake x odds`. |
| 12 | Send `GET /api/balance` again. | Persisted balance can be checked after placement. |
| 13 | Compare persisted balance with the placement response. | Persisted balance matches the balance returned by `POST /api/place-bet`. |
| 14 | Send `POST /api/reset-balance`. | Reset request is accepted. |
| 15 | Inspect the reset response status. | Status is `200`. |
| 16 | Inspect the reset response body. | Response contains `message` as a string, `balance` as a number, and `currency` equal to `EUR`. |
| 17 | Send and record the current balance using `GET /api/balance` again. | Persisted balance can be compared to the reset response. |
| 18 | Compare persisted balance with the reset response. | Persisted balance matches the reset response. |

**Invalid Request and Error-Class Checks:**

| Step | Action | Expected Result / Validation |
|---:|---|---|
| 19 | Send invalid `POST /api/place-bet` requests, for example invalid stake `100.01`, missing `x-user-id`, and invalid selection value such as `INVALID`. | Invalid requests are rejected. |
| 20 | Check balance after invalid requests. | Balance remains unchanged and no invalid bet is created. |
| 21 | Exercise expected API error classes for invalid requests. | Malformed or non-object payload is rejected with `400`; missing or invalid `x-user-id` is rejected with `401`; unsupported HTTP method is rejected with `405`; semantic validation failures for invalid `selection`, `stake`, or `matchId` are rejected with `422`. |
| 22 | If a same-user “bet already in progress” state can be triggered, send a request in that state. | API returns `409`. |
| 23 | Note uncontrolled server failures. | `500` is an unexpected server failure class and is not covered as a deterministic manual test unless controlled failure injection or a mock is available. |
| 24 | Send a valid `POST /api/place-bet` request with an extra unsupported field. | Request is accepted. |
| 25 | Inspect the response status. | Status is `200`. |
| 26 | Compare response and balance values with a normal valid placement. | Extra field does not affect bet placement, payout calculation, balance, or response consistency. |

**Expected Result Summary:**
- `GET /api/matches` returns `200` and a valid match list contract.
- Each match contains required match details and numeric odds values.
- `GET /api/balance` returns `200`, current balance, and `currency: EUR`.
- Valid `POST /api/place-bet` returns `200` and creates a bet.
- Bet placement response contains consistent `matchId`, `selection`, `stake`, `odds`, `payout`, updated `balance`, and `currency: EUR`.
- Payout is calculated as `stake x odds`.
- Balance returned by `POST /api/place-bet` is consistent with the persisted balance from `GET /api/balance`.
- `POST /api/reset-balance` returns `200` and resets the balance.
- Reset response and persisted balance are consistent.
- Invalid bet placement request is rejected.
- No invalid bet is created.
- Balance remains unchanged after rejected invalid request.
- Extra unsupported fields do not break a valid `POST /api/place-bet` request.
- Extra unsupported fields are ignored and do not affect odds, payout, balance, or response consistency.

---
