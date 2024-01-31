from fastapi import FastAPI
from pytest import fixture
from starlette.testclient import TestClient

from firstlib.infra.fastapi import FastApiConfig
from firstlib.runner.factory import InMemoryInfraFactory


@fixture
def app() -> FastAPI:
    return FastApiConfig(infra=InMemoryInfraFactory()).setup()


@fixture
def http(app: FastAPI) -> TestClient:
    return TestClient(app)
