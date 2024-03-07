ARG venv=/opt/.venv

# TODO: need to double check image :]
FROM python:3.10.13-slim-bullseye AS install-base
ARG YOUR_ENV
ARG venv
WORKDIR /opt/nlp-stock-sa
ENV PATH="/root/.poetry/bin:$PATH"
ENV VIRTUAL_ENV=$venv
ENV PYTHONUNBUFFERED 1
ENV FORCE_COLOR 1
RUN apt-get update
RUN apt-get install --no-install-recommends -y libssl-dev build-essential vim nano \
    && python -m venv $venv \
    && pip install poetry==1.7.1

FROM install-base AS install-dev
COPY server/pytest.ini server/pyproject.toml server/poetry.lock server/.poetry-cache ./
RUN poetry config cache-dir .poetry-cache
RUN poetry install --no-root --no-interaction
RUN useradd --uid 2000 nlpssa_app
RUN chown -R nlpssa_app:nlpssa_app /opt/.venv

FROM python:3.10.13-slim-bullseye AS dev-base
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install --no-install-recommends -y libssl-dev vim nano
RUN mkdir -p /var/log/nlp-stock-sa
RUN useradd --uid 2000 nlpssa_app
USER nlpssa_app
ARG venv
WORKDIR /opt/nlp-stock-sa
ENV PATH="$venv/bin:$PATH"
# TODO: not sure about this one :)
ENV PYTHONPATH="api/:$PYTHONPATH"
ENV PYTHONPATH="db/:$PYTHONPATH"
COPY --from=install-dev /opt/.venv /opt/.venv

FROM dev-base AS server-dev
ARG HOST
ARG PORT
CMD ["uvicorn", "server.api.app:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]

FROM dev-base AS ssa-dev
CMD poetry run server/ssa/scraper/main.py

FROM install-base AS install-release
COPY server/pyproject.toml server/poetry.lock ./
RUN poetry install --no-root --no-interaction --no-dev
RUN useradd --uid 2000 nlpssa_app
RUN chown -R nlpssa_app:nlpssa_app /opt/.venv

FROM python:3.10.13-slim-bullseye AS release-base
RUN apt-get update
RUN apt-get install --no-install-recommends -y libssl-dev vim nano
RUN useradd --uid 2000 nlpssa_app
RUN mkdir -p /var/log/nlp-stock-sa/server
RUN chown -R nlpssa_app:nlpssa_app /var/log/nlp-stock-sa/server
USER nlpssa_app
ARG venv
WORKDIR /opt/nlp-stock-sa/server
ENV PATH="$venv/bin:$PATH"
# TODO: not sure about this one :)
ENV PYTHONPATH="server/:$PYTHONPATH"
COPY --from=install-release /opt/.venv /opt/.venv
COPY --from=install-release /opt/nlp-stock-sa/server/ ./
COPY server/scraper ./server/scraper
# TODO: might need something like this for DB migrations after we set up the database
# COPY server/alembic.ini ./

# Maybe server-api? api-server?
FROM release-base AS server
ARG HOST
ARG PORT

CMD uvicorn api.app:app --host $HOST --port $PORT
# ^ may need to change this command

