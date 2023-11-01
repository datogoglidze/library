from pytest import fixture
from starlette.testclient import TestClient

from firstlib.infra.fastapi import FastApiConfig
from firstlib.infra.http import Httpx
from tests.client import FirstlibApi


@fixture
def http() -> TestClient:
    return TestClient(FastApiConfig().setup())


@fixture
def firstlib(http: Httpx) -> FirstlibApi:
    return FirstlibApi(http)
