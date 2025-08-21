#!/bin/bash

getDatabaseContainerID() {
    docker ps -qf name=database
}

getDatabaseHost() {
    docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(getDatabaseContainerID)
}

DATABASE_NAME="the_money_maker"
TEST_DATABASE_NAME="test_the_money_maker"
# https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING-URIS
PSQL_CONNECTION="postgresql://postgres:example@database:5432"
LAST_RETURN_STATUS_CODE=$?


# If you do not want that output, use...
# -- `>/dev/null` to suppress stdout
# -- `2>/dev/null` to suppress stderr
# -- `&>/dev/null` to suppress both

dbIsNotReady() {
    pg_isready -h database > /dev/null 2>&1;
    return $(( $? == 0 ? 1 : 0 ));  # Flip the exit code: return 1 if ready, 0 if not ready
}

isDbReady() {
    # docker compose up -d database 1> /dev/null &
    echo ""
    echo "======================================================================================"
    echo "Starting ready loop..."
    echo "======================================================================================"
    echo ""
    while dbIsNotReady; do
    # while ! pg_isready -h database >/dev/null 2>&1; do
        echo "Waiting for database to be ready..."
        echo "Container ID: $(getDatabaseContainerID)"
        echo "Database Host: $(getDatabaseHost)"
        sleep 2
    done
}

dbExists() {
    # TODO: fix this... it doesn't work as expected
    [ "$(psql $PSQL_CONNECTION -l | grep $DATABASE_NAME | wc -l)" -ne 0 ]
}

dropDatabase() {
    echo ""
    echo "======================================================================================"
    echo "Dropping $DATABASE_NAME database..."
    echo "======================================================================================"
    echo ""
    docker compose exec database \
        psql $PSQL_CONNECTION \
        -c "DROP DATABASE IF EXISTS $DATABASE_NAME"
}

dropTestDatabase() {
    echo ""
    echo "======================================================================================"
    echo "Dropping $TEST_DATABASE_NAME database..."
    echo "======================================================================================"
    echo ""
    docker compose exec database \
        psql $PSQL_CONNECTION \
        -c "DROP DATABASE IF EXISTS $TEST_DATABASE_NAME"
}

createDatabase() {
    if [[ $* == "-d" ]]; then # drop flag included
        dropDatabase
    fi

    docker compose exec database \
        psql $PSQL_CONNECTION \
        -f "/opt/db/scripts/init_db.sql"

    docker compose run --rm server python nlp_ssa/scripts/db/initialize.py
}

createTestDatabase() {
    if [[ $* == "-d" ]]; then # drop flag included
        dropTestDatabase
    fi

    docker compose exec database \
        psql $PSQL_CONNECTION \
        -f "/opt/db/scripts/init_test_db.sql"

    docker compose run \
        -e DATABASE_NAME=$TEST_DATABASE_NAME \
        -e ENV=test \
        --rm server python nlp_ssa/scripts/db/initialize.py
}

initDatabase() {
    isDbReady

    if [[ $* == "-d" || ! $(dbExists) ]]; then
        echo ""
        echo "======================================================================================"
        echo "Creating $DATABASE_NAME database..."
        echo "======================================================================================"
        echo ""
        createDatabase
    else
        echo ""
        echo "======================================================================================"
        echo "$DATABASE_NAME already exists :]"
        echo "======================================================================================"
        echo ""
    fi
}

initTestDatabase() {
    isDbReady

    if [[ $* == "-d" || ! $(dbExists) ]]; then
        echo ""
        echo "======================================================================================"
        echo "Creating $TEST_DATABASE_NAME database..."
        echo "======================================================================================"
        echo ""
        createTestDatabase
    else
        echo ""
        echo "======================================================================================"
        echo "$TEST_DATABASE_NAME already exists :]"
        echo "======================================================================================"
        echo ""
    fi
}

seedDatabase() {
    isDbReady

    if [[ ! $(dbExists) ]]; then
        docker compose run --rm server python nlp_ssa/scripts/db/seeding/seed_db.py
    fi
}

seedStocks() {
    isDbReady

    if [[ ! $(dbExists) ]]; then
        docker compose run --rm server python nlp_ssa/scripts/db/seeding/seed_stocks.py
    fi
}

cleanDocker() {
    echo "1) Prune containers"
    docker container prune -f # & fg

    echo "2) Prune images"
    docker image prune -f # & fg

    echo "3) Prune volumes"
    docker volume prune -f # & fg

    echo "4) Prune networks"
    docker network prune -f # & fg
}

scriptController() {
    # TODO: fix this case :]
    if [ "$1" == "dcr-alembic" ]; then
        echo "before: $@"
        shift
        echo "after: $@"
        while getopts "m" arg; do
            echo "m arg: ${$arg}"
            case ${arg} in
                m)
                    echo "m: "${$OPTARG}
                    docker compose run --rm server alembic revision --autogenerate -m "'${OPTARG}'"
                    exit 0
                    ;;
            esac
        done
    elif [ "$1" == "db" ]; then
        echo ""
        echo "======================================================================================"
        echo "db case"
        echo "======================================================================================"
        echo ""
        if [ "$2" == "drop" ]; then
            dropDatabase
        elif [ "$2" == "drop-test" ]; then
            dropTestDatabase
        elif [ "$2" == "sandbox" ]; then
            docker compose run --rm server python nlp_ssa/scripts/db/sandbox.py
        elif [ "$2" == "stash" ]; then
            docker compose run --rm server python nlp_ssa/scripts/db/stash_db.py
        elif [ "$2" == "pop" ]; then
            docker compose run --rm server python nlp_ssa/scripts/db/pop_db.py
        elif [ "$2" == "up-head" ]; then
            docker compose run --rm server alembic upgrade head
        elif [ "$2" == "down-1" ]; then
            docker compose run --rm server alembic downgrade -1
        elif [ "$2" == "init" ]; then
            echo ""
            echo "======================================================================================"
            echo "Initializing $DATABASE_NAME database..."
            echo "======================================================================================"
            echo ""
            initDatabase
        elif [ "$2" == "create" ]; then
            echo ""
            echo "======================================================================================"
            echo "Creating $DATABASE_NAME database..."
            echo "======================================================================================"
            echo ""
            createDatabase
        elif [ "$2" == "init-test" ]; then
            echo ""
            echo "======================================================================================"
            echo "Initializing test_$DATABASE_NAME database..."
            echo "======================================================================================"
            echo ""
            initTestDatabase
        elif [ "$2" == "create-test" ]; then
            echo ""
            echo "======================================================================================"
            echo "Creating test_$DATABASE_NAME database..."
            echo "======================================================================================"
            echo ""
            createTestDatabase
        elif [ "$2" == "seed" ]; then
            if [ "$3" == "stocks" ]; then
                echo ""
                echo "======================================================================================"
                echo "Seeding stocks data..."
                echo "======================================================================================"
                echo ""
                seedStocks
            else
                echo ""
                echo "======================================================================================"
                echo "Seeding database..."
                echo "======================================================================================"
                echo ""
                seedDatabase
            fi
        fi
    elif [ "$1" == "frontend" ]; then
        if [ "$2" == "rebuild" ]; then
            echo ""
            echo "======================================================================================"
            echo "Rebuilding frontend..."
            echo "======================================================================================"
            echo ""
            docker compose down frontend && \
            docker compose build frontend --no-cache && \
            docker compose up frontend -d && \
            docker image prune -f
        fi
    elif [ "$1" == "run" ]; then
        if [ "$2" == "scraper" ]; then
            echo ""
            echo "======================================================================================"
            echo "Rebuilding and running scraper..."
            echo "======================================================================================"
            echo ""
            docker compose up scraper --build -d
        elif [ "$2" == "ssa" ]; then
            echo ""
            echo "======================================================================================"
            echo "Running 'stock_sentiment_analysis' script..."
            echo "======================================================================================"
            echo ""
            docker compose run --rm server python nlp_ssa/scripts/analysis/ssa.py
        elif [ "$2" == "clean-ad" ]; then
            echo ""
            echo "======================================================================================"
            echo "Running 'clean_article_data' script..."
            echo "======================================================================================"
            echo ""
            docker compose run --rm server python nlp_ssa/scripts/data_cleaning/clean_article_data.py
        elif [ "$2" == "del-orph-sa" ]; then
            echo ""
            echo "======================================================================================"
            echo "Running 'delete_orphaned_sentiment_analyses' script..."
            echo "======================================================================================"
            echo ""
            docker compose run --rm server python nlp_ssa/scripts/data_cleaning/delete_orphaned_sentiment_analyses.py
        elif [ "$2" == "ad-to-csv" ]; then
            echo ""
            echo "======================================================================================"
            echo "Running 'article_data_as_csv' script..."
            echo "======================================================================================"
            echo ""
            docker compose run --rm server python nlp_ssa/scripts/downloads/article_data_as_csv.py
        fi
    elif [ "$1" == "test" ]; then
        if [ "$2" == "server" ]; then
            echo ""
            echo "======================================================================================"
            echo "Running server tests! :D"
            echo "======================================================================================"
            echo ""
            docker compose run \
                -e DATABASE_NAME=test_the_money_maker \
                -e ENV=test \
                --rm server python \
                -m pytest \
                -s --import-mode=append  # "'${@:3}'"
        fi
    elif [ "$1" == "clean" ]; then
        echo ""
        echo "======================================================================================"
        echo "clean case"
        echo "======================================================================================"
        echo ""
        if [ "$2" == "docker" ]; then
            cleanDocker
        fi
    elif [ "$1" == "reset-server" ]; then
        docker compose down && \
        docker compose build database server --no-cache && \
        docker compose up -d database server
    fi
}

scriptController $@
