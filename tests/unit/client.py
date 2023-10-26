from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

import httpx
from starlette.testclient import TestClient

from firstlib.infra.http import HttpUrl


@dataclass
class RestResource:
    http: TestClient
    name: RestfulName

    def parse(self, response: httpx.Response) -> RestEnvelope:
        return RestEnvelope(
            resource=self.name.singular,
            json=response.json(),
            http_code=response.status_code,
        )

    def create_one(self, from_data: dict[str, Any]) -> RestEnvelope:
        return self.parse(self.http.post(self.name + "", json=from_data))

    def read_one(self, with_id: str | UUID) -> RestEnvelope:
        return self.parse(self.http.get(self.name + str(with_id)))

    def read_all(self) -> RestEnvelope:
        return self.parse(self.http.get(self.name + ""))

    def update_one(self, with_id: str | UUID, and_data: dict[str, Any]) -> RestEnvelope:
        return self.parse(self.http.patch(self.name + str(with_id), json=and_data))


@dataclass
class RestfulName:
    singular: str

    plural: str = ""

    def __post_init__(self) -> None:
        if self.singular.endswith("y"):
            plural = self.singular[:-1] + "ies"
        else:
            plural = self.singular + "s"
        self.plural = self.plural or plural

    def __add__(self, other: str) -> str:
        return HttpUrl(self.plural) + other


@dataclass
class RestEnvelope:
    json: dict[str, Any]
    http_code: int
    resource: str

    def unpack(self, exclude: list[str] | None = None) -> dict[str, Any]:
        return {
            key: value
            for key, value in self.json["data"][self.resource].items()
            if key not in (exclude or [])
        }

    def __getitem__(self, item: str) -> Any:
        return self.unpack()[item]

    def assert_ok(self, **kwargs: Any) -> None:
        self.assert_success(200, with_data={**kwargs})

    def assert_created(self, **kwargs: Any) -> None:
        self.assert_success(201, with_data={**kwargs})

    def assert_success(self, code: int, with_data: dict[str, Any]) -> None:
        self._assert(
            code,
            with_json={
                "status": "success",
                "code": code,
                "data": with_data,
            },
        )

    def _assert(self, expected_code: int, with_json: dict[str, Any]) -> None:
        assert self.http_code == expected_code, self.json
        assert self.json == with_json, self.json

    def assert_bad_request(self, with_message: str, and_data: dict[str, Any]) -> None:
        self.assert_fail(400, with_message, and_data)

    def assert_not_found(self, with_message: str) -> None:
        self.assert_fail(404, with_message)

    def assert_conflict(self, with_message: str) -> None:
        self.assert_fail(409, with_message)

    def assert_invalid(self, with_detail: dict[str, Any]) -> None:
        self._assert(422, with_json={"detail": [with_detail]})

    def assert_fail(
        self,
        code: int,
        with_message: str,
        and_data: dict[str, Any] | None = None,
    ) -> None:
        json = {
            "status": "fail",
            "code": code,
            "error": {"message": with_message},
        }

        if and_data is not None:
            json["data"] = and_data

        self._assert(code, with_json=json)
