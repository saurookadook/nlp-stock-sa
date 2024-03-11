# NLP Stock SA

This is a stock sentiment analysis project.

Resources:
- [DB potential schema- lucidchart](https://lucid.app/lucidchart/1723ceb6-2878-41eb-8635-b7ee19a8b545/edit?view_items=4xwL7nak7NXS&invitationId=inv_baa67f02-3606-4521-813e-1aaadd75bb81)
- [Example DB tables](https://docs.google.com/drawings/d/16xttDCvKXwcfHAD_Jk_BNj3nUYusFEAdXT9sMvCwBWU/edit?usp=sharing)
- [General pipeline - graph](https://docs.google.com/drawings/d/1MXKg1cNiAlD6T-5AAXAwya8o7Z69hFH9PmhIVDQ_Vmw/edit?usp=sharing)
- [General pipeline building](https://docs.google.com/document/d/1czS0XXaNHYZwbpxwVmxxbbdjS-T6AESQo0vkFuzelPk/edit?usp=sharing)


## Requirements

- Docker
- Python 3.10
- Poetry 1.7.1
- Node 18.19.0
- Yarn 4.1.0
- PostgreSQL 16.2.0

<!-- TODO: include download links :] -->

## Installation

Add following to `/etc/hosts`

```
127.0.0.1 nlp-stock-sa.com database
```

> **NOTE: For M1 only**
>
> ```sh
> export DOCKER_DEFAULT_PLATFORM=linux/amd64
> ```

```sh
$ brew install nvm yarn python@3.10.4 postgresql@16
# For M1 Mac only
$ /opt/homebrew/bin/createuser -s postgres
$ curl -sSL https://install.python-poetry.org | python 3 -
$ nvm install $(cat .nvmrc) && nvm use
```

### Bare `.env`

```
HOST="0.0.0.0"
PORT=3000
LOG_LEVEL=INFO
POETRY_CACHE_DIR=ssa/.poetry-cache

POSTGRES_DB=the_money_maker
POSTGRES_USER=postgres
POSTGRES_PASSWORD=example
```


## Installing Required Software

### Docker

_TODO_ 🫠

### PostgreSQL

```sh
$ brew install postgresql@16
$ brew services stop postgresql@16 # <= need to stop server started by Homebrew as it'll interfere with our container
```

### Python

_TODO_ 🫠

### Poetry

_TODO_ 🫠

### Node

_TODO_ 🫠

### Yarn

_TODO_ 🫠


## Operations??

### DB Migrations

Run current database migrations:

```sh
$ docker-compose run --rm server alembic upgrade head
```

Reset to base version

```sh
$ docker-compose run --rm server alembic downgrade
```

Run revisions:

```sh
$ docker-compose run --rm server alembic revision -m "some migration message"
```

Autogenerate revisions:

```sh
$ docker-compose run --rm server alembic revision --autogenerate -m "some migration message"
```

## Tests

### Server

Run current database migrations for test database:

```sh
$ docker-compose run -e DATABASE_NAME=test_the_money_maker server alembic upgrade head
```

Run tests with:

```sh
$ docker-compose run -e DATABASE_NAME=test_the_money_maker -e ENV=test --rm server python -m pytest -s --import-mode=append
```

Or run in watch mode:

```sh
$ docker-compose run -e DATABASE_NAME=test_the_money_maker -e ENV=test --rm server pytest-watch
```
