from __future__ import annotations

import logging.config
from dataclasses import dataclass
from typing import Any, Self

import typer
import uvicorn
from dotenv import load_dotenv
from typer import Typer, echo

from firstlib.infra.fastapi import FastApiConfig
from firstlib.runner.factory import InMemoryInfraFactory

cli = Typer(no_args_is_help=True, add_completion=False)


@cli.command()
def run(host: str = "0.0.0.0", port: int = 8100) -> None:
    typer.echo(f"Running application on {host}:{port}")
    load_dotenv()
    LoggingConfig.from_env().setup()
    uvicorn.run(
        host=host,
        port=port,
        app=FastApiConfig(infra=infra_factory()).setup(),
        log_config=LoggingConfig.from_env().as_dict(),
    )


def infra_factory() -> InMemoryInfraFactory:
    echo("Using in-memory storage...")
    return InMemoryInfraFactory()


@dataclass
class LoggingConfig:
    level: int

    @classmethod
    def from_env(cls) -> Self:
        return cls(logging.INFO)

    def setup(self) -> None:
        logging.config.dictConfig(self.as_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard",
                    "level": self.level,
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "standard",
                    "level": self.level,
                    "filename": "app.log",
                    "maxBytes": 1024 * 1024,
                    "backupCount": 10,
                },
            },
            "loggers": {
                "": {
                    "handlers": ["console", "file"],
                    "level": self.level,
                    "propagate": False,
                },
            },
            "uvicorn": {
                "handlers": ["console", "file"],
                "level": self.level,
                "propagate": False,
            },
        }
