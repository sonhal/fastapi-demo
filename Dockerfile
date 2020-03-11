FROM python:3.7-slim as build

LABEL maintainer="sonhal"

RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.in-project true && poetry install --no-root --no-interaction
COPY fastapi_demo /app/fastapi_demo/
COPY tests /app/tests/
RUN poetry run pytest
RUN poetry install --no-dev --no-interaction

FROM python:3.7-slim

COPY --from=build /app/.venv /app/.venv/
COPY --from=build /app/fastapi_demo /app/fastapi_demo/

COPY gunicorn_conf.py /app/gunicorn_conf.py

EXPOSE 8080
# To make mouting of HTML from static/ in fastapi_demo work
WORKDIR /app

CMD [".venv/bin/gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--config", "gunicorn_conf.py", "fastapi_demo.main:app"]
