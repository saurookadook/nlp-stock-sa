ARG venv=/opt/.venv

# TODO: need to double check image :]
FROM python:3.10.13-slim-bullseye AS install-base
ARG YOUR_ENV
ARG venv
WORKDIR /opt/nlp-stock-sa/server
ENV PATH="/root/.poetry/bin:$PATH"
ENV VIRTUAL_ENV=$venv
ENV PYTHONUNBUFFERED=1
ENV FORCE_COLOR=1
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
ENV PYTHONUNBUFFERED=1
RUN apt-get update
RUN apt-get install --no-install-recommends -y libssl-dev vim nano
RUN mkdir -p /var/log/nlp-stock-sa
RUN useradd --uid 2000 nlpssa_app
RUN mkdir -p /opt/.venv
RUN chown -R nlpssa_app:nlpssa_app /opt/.venv
USER nlpssa_app
ARG venv
WORKDIR /opt/nlp-stock-sa/server
ENV PATH="$venv/bin:$PATH"
ENV PYTHONPATH="/opt/nlp-stock-sa/server/nlp_ssa/:$PYTHONPATH"
COPY --from=install-dev /opt/.venv /opt/.venv

FROM dev-base AS server-dev
ARG HOST
ARG PORT
ENV PYTHONUNBUFFERED=1
ENV FORCE_COLOR=1
# TODO: figure out why $HOST and $PORT aren't getting interpolated correctly
EXPOSE 3000
ENTRYPOINT ["uvicorn", "nlp_ssa.api.app:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]

FROM dev-base AS scraper-dev
ENV PATH="$venv/bin:$PATH"
ENV PYTHONPATH="/opt/nlp-stock-sa/server/nlp_ssa/:$PYTHONPATH"
USER root
WORKDIR /opt/nlp-stock-sa/server
ENTRYPOINT [ "python3", "nlp_ssa/scraper/main.py" ]

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
ENV PYTHONPATH="nlp_ssa/:$PYTHONPATH"
COPY --from=install-release /opt/.venv /opt/.venv
COPY --from=install-release /opt/nlp-stock-sa/server/ ./
COPY server/scraper ./server/scraper
COPY server/alembic.ini ./

# Maybe server-api? api-server?
FROM release-base AS server
ARG HOST
ARG PORT

ENTRYPOINT [ "uvicorn", "api.app:app", "--host", "$HOST", "--port", "$PORT" ]
# ^ may need to change this command

