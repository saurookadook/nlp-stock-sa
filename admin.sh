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
PSQL_CONNECTION="postgresql://postgres:example@database"
LAST_RETURN_STATUS_CODE=$?


# If you do not want that output, use...
# -- `>/dev/null` to suppress stdout
# -- `2>/dev/null` to suppress stderr
# -- `&>/dev/null` to suppress both

dbIsNotReady() {
    pg_isready -h database
    [[ $? -ne 0 ]]
}

isDbReady() {
    # docker-compose up -d database 1> /dev/null &
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

createDatabase() {
    if [[ $* == "-d" ]]; then # drop flag included
        echo ""
        echo "======================================================================================"
        echo "Dropping $DATABASE_NAME database..."
        echo "======================================================================================"
        echo ""
        psql $PSQL_CONNECTION -c "DROP DATABASE IF EXISTS $DATABASE_NAME"
    fi

    psql $PSQL_CONNECTION -f "db/init_db.sql"
    docker-compose run --rm server python nlp_ssa/scripts/db/initialize.py
}

createTestDatabase() {
    if [[ $* == "-d" ]]; then # drop flag included
        psql $PSQL_CONNECTION -c DROP DATABASE IF EXISTS $DATABASE_NAME
    fi

    psql $PSQL_CONNECTION -f "db/init_test_db.sql"
    docker-compose run -e "DATABASE_NAME=test_the_money_maker" --rm server python nlp_ssa/scripts/db/initialize.py
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
        # echo ""
        # echo "======================================================================================"
        # echo "$DATABASE_NAME already exists :]"
        # echo "======================================================================================"
        # echo ""
    else
        echo ""
        echo "======================================================================================"
        echo "$DATABASE_NAME already exists :]"
        echo "======================================================================================"
        echo ""
        # echo "======================================================================================"
        # echo "Creating $DATABASE_NAME database..."
        # echo "======================================================================================"
        # createDatabase
    fi
}

initTestDatabase() {
    isDbReady

    if dbExists; then
        echo ""
        echo "======================================================================================"
        echo "$TEST_DATABASE_NAME already exists :]"
        echo "======================================================================================"
        echo ""
    else
        echo ""
        echo "======================================================================================"
        echo "Creating $TEST_DATABASE_NAME database..."
        echo "======================================================================================"
        echo ""
        createTestDatabase
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
    if [ "$1" == "db" ]; then
        echo ""
        echo "======================================================================================"
        echo "db case"
        echo "======================================================================================"
        echo ""
        if [ "$2" == "init" ]; then
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
            echo "Initializing $TEST_DATABASE_NAME database..."
            echo "======================================================================================"
            echo ""
            initTestDatabase
        elif [ "$2" == "create-test" ]; then
            echo ""
            echo "======================================================================================"
            echo "Creating $TEST_DATABASE_NAME database..."
            echo "======================================================================================"
            echo ""
            createTestDatabase
        fi
    elif [ "$1" == "db-check" ]; then
        echo ""
        echo "======================================================================================"
        echo "Checking if $DATABASE_NAME exists... $(dbExists)"
        echo "======================================================================================"
        echo ""
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
        docker-compose down && docker-compose build database server --no-cache && docker-compose up -d database server
    elif [ "$1" == "test" ]; then
        echo "testing..."
        # for testing individual things :]
    fi
}

scriptController $@
