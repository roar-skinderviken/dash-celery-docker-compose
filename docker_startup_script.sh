#!/bin/bash

# Start Dash app
gunicorn --config ./gunicorn.conf.py "dash_app.wsgi:server" &

# Start Celery worker
celery -A dash_app.app.celery_app worker --loglevel=info &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?