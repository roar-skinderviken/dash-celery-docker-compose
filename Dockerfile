ARG PACKAGE_NAME=dash_app
ARG PYTHON_VERSION=3.11-slim-bullseye

FROM python:$PYTHON_VERSION AS builder
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Poetry
RUN pip install poetry==1.6.1

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md \
    && poetry config cache-dir "$POETRY_CACHE_DIR" \
    && poetry install --no-root

FROM python:$PYTHON_VERSION AS runtime
ARG PACKAGE_NAME
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PACKAGE_NAME=$PACKAGE_NAME

RUN useradd --create-home appuser
USER appuser

# Copy virtual environment
COPY --from=builder --chown=appuser ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy application code
COPY src/$PACKAGE_NAME ./$PACKAGE_NAME
COPY --chown=appuser gunicorn.conf.py docker_startup_script.sh ./

# Change permissions
RUN chmod -R a-w ${VIRTUAL_ENV} \
    && chmod a-w gunicorn.conf.py \
    && chmod a-w+x ./docker_startup_script.sh

# Running the application
CMD ./docker_startup_script.sh
