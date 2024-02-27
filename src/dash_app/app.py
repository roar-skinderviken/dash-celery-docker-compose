import logging
import os

import dash
import diskcache
from celery import Celery
from dash import Dash, DiskcacheManager, CeleryManager, html

logger = logging.getLogger(__name__)

# some constants
DEFAULT_PORT: int = 7002
REDIS_HOST = "redis://dash-app-redis:6379"
DOCKER_ENV = "docker"

# get the running environment
RUNNING_ENV = os.environ.get("RUNNING_ENV")

# expose the celery app only if we are running in docker
celery_app = Celery(
    __name__,
    broker=f"{REDIS_HOST}/0",
    backend=f"{REDIS_HOST}/1",
) if RUNNING_ENV == DOCKER_ENV else None


def get_background_callback_manager():
    if RUNNING_ENV == DOCKER_ENV:
        return CeleryManager(celery_app)
    else:
        return DiskcacheManager(diskcache.Cache("./cache"))


# keep the background callback manager in a global variable
_background_callback_manager = get_background_callback_manager()


def get_app() -> Dash:
    app = Dash(
        name=__name__,
        title="Dash POC",
        background_callback_manager=_background_callback_manager,
        use_pages=True
    )

    app.layout = html.Div(
        dash.page_container
    )

    return app


def main() -> None:
    logging.basicConfig(level=logging.DEBUG, force=True)
    logger.info("Starting app")
    app = get_app()

    logger.debug("Starting in development mode")
    app.run(
        debug=True,
        port=DEFAULT_PORT
    )


if __name__ == "__main__":
    main()
