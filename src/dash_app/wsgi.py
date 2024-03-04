"""Entrypoint for Gunicorn."""
from dash_app.app import app
server = app.server
