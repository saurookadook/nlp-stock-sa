ARG venv=/opt/.venv

# TODO: need to double check image :]
FROM python:3.10.13-slim-bullseye AS install-base
ARG YOUR_ENV
ARG venv
WORKDIR /opt/nlp-stock-sa/ssa
ENV PATH="/root/.poetry/bin:$PATH"
ENV VIRTUAL_ENV=$venv
ENV PYTHONUNBUFFERED 1
ENV FORCE_COLOR 1
RUN apt-get update
RUN apt-get install --no-install-recommends -y libssl-dev build-essential vim nano \
    && python -m venv $venv \
    && pip install poetry==1.7.1

FROM install-base AS install-dev
COPY ssa/pytest.ini ssa/pyproject.toml ssa/poetry.lock ssa/.poetry-cache ./
RUN poetry config cache-dir .poetry-cache
RUN poetry install --no-root --no-interaction
RUN useradd --uid 2000 nlpstocksaapp
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/.venv

FROM python:3.10.13-slim-bullseye AS dev-base
ENV PYTHONUNBUFFERED 1
RUN apt-get update
RUN apt-get install --no-install-recommends -y libssl-dev vim nano
RUN mkdir -p /var/log/nlp-stock-sa/ssa
RUN useradd --uid 2000 nlpstocksaapp
USER nlpstocksaapp
ARG venv
WORKDIR /opt/nlp-stock-sa/ssa
ENV PATH="$venv/bin:$PATH"
# TODO: not sure about this one :)
ENV PYTHONPATH="ssa/:$PYTHONPATH"
COPY --from=install-dev /opt/.venv /opt/.venv

FROM dev-base AS ssa-dev
CMD poetry run ssa/scraper/main.py

FROM install-base AS install-release
COPY ssa/pyproject.toml ssa/poetry.lock ./
RUN poetry install --no-root --no-interaction --no-dev
RUN useradd --uid 2000 nlpstocksaapp
RUN chown -R nlpstocksaapp:nlpstocksaapp /opt/.venv

FROM python:3.10.13-slim-bullseye AS release-base
RUN apt-get update
RUN apt-get install --no-install-recommends -y libssl-dev vim nano
RUN useradd --uid 2000 nlpstocksaapp
RUN mkdir -p /var/log/nlp-stock-sa/ssa
RUN chown -R nlpstocksaapp:nlpstocksaapp /var/log/nlp-stock-sa/ssa
USER nlpstocksaapp
ARG venv
WORKDIR /opt/nlp-stock-sa/ssa
ENV PATH="$venv/bin:$PATH"
# TODO: not sure about this one :)
ENV PYTHONPATH="ssa/:$PYTHONPATH"
COPY --from=install-release /opt/.venv /opt/.venv
COPY --from=install-release /opt/nlp-stock-sa/ssa/ ./
COPY ssa/scraper ./scraper
# TODO: might need something like this for DB migrations after we set up the database
# COPY ssa/alembic.ini ./

