# Strategy and Recommendations

## Testing Strategy

The testing approach is risk-based and intentionally focused on the Single Bet Placement flow.

The highest-value user journey is covered by one Selenium E2E test: selecting an upcoming match, entering a valid stake, checking bet slip calculations, placing the bet, checking the receipt, and validating post-bet balance behaviour.

The API layer is covered by one direct validation/business-rule test: maximum stake rejection. This was selected because the API is the final control before a bet is accepted, and frontend validation can be bypassed.

Manual coverage is documented in the [test plan](test_plan.md), with execution evidence and defects summarized in [execution results](execution_results.md) and [bug reports](bug_reports.md).

## Current Quality Picture

The application supports the main betting flow, but several high-risk defects affect trust and financial correctness:

| Priority | Area | Finding |
|---|---|---|
| P0 | Event eligibility | Past matches are shown as available betting events. |
| P0 | Receipt accuracy | Receipt payout is incorrect and match order is reversed. |
| P0 | UI balance state | Header balance stays stale after accepted bet until page refresh. |
| P0 | Balance state | Reset response and persisted balance disagree. |
| P1 | Receipt completeness | Selected outcome is missing from the receipt. |
| P1 | API consistency | `POST /api/place-bet` returns `USD` while the product uses EUR. |
| P1 | API error handling | Malformed JSON returns `500` instead of `400`. |
| P2 | Match metadata and filters | Kickoff metadata and odds filter boundaries do not fully match requirements. |

## Recommendations

1. Fix event eligibility first.  
   Past events should not appear in the upcoming match list or be available for betting. This is the most serious product risk because it may allow bets on already-known outcomes.

2. Fix receipt financial correctness before expanding UI automation.  
   Receipt payout, match order, selected outcome, and post-bet balance must be consistent with the bet slip and API response. The header balance currently stays stale after placement and only updates after page refresh; it should update immediately after a successful bet. Until then, the UI test should remain under strict `xfail`.

3. Align API financial state and currency.  
   All money-related API responses should use the same currency and balance source of truth. Currently, `POST /api/place-bet` creates the bet correctly but returns `currency: USD`, while the UI and `GET /api/balance` use EUR. This should be corrected so successful placement returns `currency: EUR`.

   Reset behaviour also needs to be consistent. `POST /api/reset-balance` currently reports one balance value, but the next `GET /api/balance` returns a different persisted value. After reset, the reset response and the persisted balance should match exactly. Otherwise users, UI checks, and automation cannot reliably know the real account balance.

4. Improve API error classification.  
   Malformed JSON is a client error and should return `400`, not `500`. This makes API behaviour easier to debug and keeps error classes aligned with the specification.

5. Expand automation only after P0 fixes.  
   The next useful automated cases would be:
   - receipt success path after defects are fixed;
   - API malformed JSON and currency contract checks;
   - a small stake validation matrix for min, max, above max, invalid selection, and missing user.

## Release Recommendation

Do not release the Single Bet Placement feature as production-ready until the P0 issues are fixed and re-tested:

- past match availability;
- receipt payout accuracy;
- receipt match-order consistency;
- immediate post-bet header balance update;
- reset/persisted balance consistency.

After those fixes, rerun the automated UI test without `xfail` and repeat the API execution checks from [execution_results.md](execution_results.md).
