import logging
import os
import time

# import dash_bootstrap_components as dbc
import diskcache
from celery import Celery
from dash import Dash, DiskcacheManager, CeleryManager, Output, Input, callback, html

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
        background_callback_manager=_background_callback_manager
    )

    app.layout = html.Div(
        [
            html.Div([html.P(id="paragraph_id", children=["Button not clicked"])]),
            html.Button(id="button_id", children="Run Job!"),
        ]
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


@callback(
    Output("paragraph_id", "children"),
    Input("button_id", "n_clicks"),
    running=[
        (Output("button_id", "disabled"), True, False),
        (Output("button_id", "children"), "Running...", "Run Job!")
    ],
    background=True,
    prevent_initial_call=True
)
def update_clicks(n_clicks):
    time.sleep(2.0)
    return [f"Clicked {n_clicks} times"]


if __name__ == "__main__":
    main()
