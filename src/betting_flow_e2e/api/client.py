from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Self

import requests

from betting_flow_e2e.api.contracts.assertions import (
    assert_balance_contract,
    assert_matches_contract,
    assert_reset_balance_contract,
)
from betting_flow_e2e.domain.matches import MatchData, first_upcoming_match
from betting_flow_e2e.utils.money import money

type JsonObject = dict[str, Any]
type JsonValue = Any


@dataclass(frozen=True, slots=True)
class BalanceState:
    balance: Decimal
    currency: str

    @classmethod
    def from_payload(cls, payload: JsonObject) -> Self:
        return cls(
            balance=money(payload["balance"]),
            currency=str(payload["currency"]),
        )


class ApiClient:
    def __init__(
        self,
        base_url: str,
        user_id: str,
        timeout_seconds: float = 10,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        self.timeout_seconds = timeout_seconds
        self.session = session or requests.Session()

    @property
    def headers(self) -> dict[str, str]:
        return {"x-user-id": self.user_id}

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def _get_json(self, path: str) -> JsonValue:
        response = self.session.get(
            self._url(path),
            headers=self.headers,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def _post_json(self, path: str) -> JsonValue:
        response = self.session.post(
            self._url(path),
            headers=self.headers,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        return response.json()

    def get_matches(self) -> list[MatchData]:
        payload = self._get_json("/api/matches")
        assert_matches_contract(payload)
        return payload

    def get_first_upcoming_match(self) -> MatchData:
        return first_upcoming_match(self.get_matches())

    def get_balance(self) -> JsonObject:
        payload = self._get_json("/api/balance")
        assert_balance_contract(payload)
        return payload

    def get_balance_state(self) -> BalanceState:
        return BalanceState.from_payload(self.get_balance())

    def reset_balance(self) -> JsonObject:
        payload = self._post_json("/api/reset-balance")
        assert_reset_balance_contract(payload)
        return payload

    def reset_balance_state(self) -> BalanceState:
        self.reset_balance()
        return self.get_balance_state()

    def post_place_bet_raw(self, payload: JsonObject) -> requests.Response:
        return self.session.post(
            self._url("/api/place-bet"),
            headers=self.headers,
            json=payload,
            timeout=self.timeout_seconds,
        )
