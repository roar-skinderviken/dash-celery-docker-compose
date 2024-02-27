"""Entrypoint for Gunicorn."""
from dash_app.app import get_app

app = get_app()
server = app.server
