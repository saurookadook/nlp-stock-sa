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
### Extensions and Settings for VS Code

#### Extensions

- [Black](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)
- [ESLint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint)
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)
- [Prettier ESLint](https://marketplace.visualstudio.com/items?itemName=rvest.vs-code-prettier-eslint)


#### Settings

```sh
cp .vscode.example .vscode
```

### Details

For Docker, make sure you bump the resources it can be allocated:
- **CPU limit**: `16`
- **Memory limit**: `16 GB`
- **Swap**: `1.5 GB`
- **Virtual disk limit**: `160 GB`

### Installation

Add following to `/etc/hosts`

> _**TODO**: this might not be necessary still?_
```
127.0.0.1 nlp-stock-sa.com database
```

> **NOTE: For M1 Macs only**
>
> ```sh
> export DOCKER_DEFAULT_PLATFORM=linux/amd64
> ```

```sh
brew install nvm python@3.10.4 postgresql@16
curl -sSL https://install.python-poetry.org | python 3 - --version 1.8.2
nvm install $(cat .nvmrc) && nvm use
```

Create `.env`:

```sh
cp .env.example .env
```

Make scripts for reverse proxy executable and run `install.sh`:

```sh
chmod +x nginx-reverse-proxy/generate-certs.sh nginx-reverse-proxy/install.sh nginx-reverse-proxy/uninstall.sh
./nginx-reverse-proxy/install.sh
```

Initial install for frontend:

```sh
cd app
nvm use #=> this should set your Node version to 18.20.2
corepack yarn install
```

Initial install for backend:

```sh
cd server
poetry install
```

#### Required Software

##### Docker

[Download Docker Desktop](https://www.docker.com/products/docker-desktop/) and start it

##### PostgreSQL

```sh
brew install postgresql@16
brew services stop postgresql@16 # <= need to stop server started by Homebrew as it'll interfere with our container
```

##### Python & Poetry

```sh
brew install python@3.10.4
curl -sSL https://install.python-poetry.org | python 3 - --version 1.8.2
```

##### Node & Yarn

```sh
brew install nvm
nvm install $(cat .nvmrc) && nvm use
cd web
corepack enable && yarn install
```

## Operations??

### Quick Start

```sh
docker compose build
./admin.sh db init && ./admin.sh db seed
docker compose up all -d
```

Then navigate to `https://nlp-ssa.dev/app` 🙂

To run the scraper:
```sh
docker compose up scraper --build -d
```

### DB Migrations

Run current database migrations:

```sh
docker compose run --rm server alembic upgrade head
```

Reset to base version

```sh
docker compose run --rm server alembic downgrade
```

Run revisions:

```sh
docker compose run --rm server alembic revision -m "some migration message"
```

Autogenerate revisions:

```sh
docker compose run --rm server alembic revision --autogenerate -m "some migration message"
```

### Frontend

_TODO_ 🫠

## Tests

### Server

Run current database migrations for test database:

```sh
docker compose run -e DATABASE_NAME=test_the_money_maker server alembic upgrade head
```

Run tests with:

```sh
docker compose run -e DATABASE_NAME=test_the_money_maker -e ENV=test --rm server python -m pytest -s --import-mode=append
```

Or run in watch mode:

```sh
docker compose run -e DATABASE_NAME=test_the_money_maker -e ENV=test --rm server pytest-watch
```
