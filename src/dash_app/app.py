import logging
import os

import dash
from dash import Dash, DiskcacheManager, CeleryManager, html

logger = logging.getLogger(__name__)

# some constants
DEFAULT_PORT: int = 7002
REDIS_HOST = "redis://dash-app-redis:6379"

# get the running environment
REDIS_URL_ENV_VAR = "REDIS_URL"

if REDIS_URL_ENV_VAR in os.environ:
    # Use Redis & Celery if REDIS_URL set as an env variable
    from celery import Celery

    celery_app = Celery(
        __name__,
        broker=os.environ[REDIS_URL_ENV_VAR],
        backend=os.environ[REDIS_URL_ENV_VAR]
    )
    background_callback_manager = CeleryManager(celery_app=celery_app)

else:
    # Diskcache for non-production apps when developing locally
    import diskcache

    cache = diskcache.Cache("./cache")
    background_callback_manager = DiskcacheManager(cache=cache)

app = Dash(
    name=__name__,
    title="Dash POC",
    background_callback_manager=background_callback_manager,
    use_pages=True
)

app.layout = html.Div(
    dash.page_container
)


def main() -> None:
    logging.basicConfig(level=logging.DEBUG, force=True)
    logger.debug("Starting in development mode")
    app.run(
        debug=True,
        port=DEFAULT_PORT
    )


if __name__ == "__main__":
    main()
