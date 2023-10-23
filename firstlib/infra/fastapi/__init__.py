from dataclasses import dataclass

from fastapi import FastAPI

from firstlib.infra.fastapi.books import api


@dataclass
class FastApiConfig:
    pass

    def setup(self) -> FastAPI:
        app = FastAPI()
        app.include_router(api, prefix="/books")

        return app
