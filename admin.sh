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
RETURN=$?

isDbReady () {
    docker-compose up -d database &  # Run in the background
    while ! pg_isready -h database >/dev/null 2>&1; do
        echo "Waiting for database to be ready..."
        echo "Container ID: $(getDatabaseContainerID)"
        echo "Database Host: $(getDatabaseHost)"
        sleep 2
    done
}

dbExists () {
    RESULT_CODE=$(psql $PSQL_CONNECTION -l | grep -C $DATABASE_NAME)
    echo "retcode: $RESULT_CODE"
    [ $RESULT_CODE -eq 0 ]
}

createDatabase () {
    psql $PSQL_CONNECTION -c DROP DATABASE IF EXISTS $DATABASE_NAME
    psql $PSQL_CONNECTION -f ./db/init_db.sql
}

createTestDatabase () {
    if drop; # drop flag included
    then
        psql $PSQL_CONNECTION -c DROP DATABASE IF EXISTS $DATABASE_NAME
    fi
}

initDatabase () {
    isDbReady

    if dbExists; then
        echo "$DATABASE_NAME already exists :]"
    else
        echo "Creating $DATABASE_NAME database..."
        createDatabase
    fi
}

initTestDatabase () {
    isDbReady

    if dbExists;
    then
        echo "$TEST_DATABASE_NAME already exists :]"
    else
        echo "Creating $TEST_DATABASE_NAME database..."
        createTestDatabase
    fi
}

cleanDocker () {
    echo "1) Prune containers"
    docker container prune -f & fg

    echo "2) Prune images"
    docker image prune -f & fg

    echo "3) Prune volumes"
    docker volume prune -f & fg

    echo "4) Prune networks"
    docker network prune -f & fg
}

scriptController () {
    if [ "$1" == "db" ]; then
        if [ "$2" == "init" ]; then
            echo "Initializing $DATABASE_NAME database..."
            initDatabase
        elif [ "$2" == "init-test" ]; then
            initTestDatabase
        fi
    elif [ "$1" == "db-check" ]; then
        echo "Checking if $DATABASE_NAME exists... $(dbExists)"
    fi
}

scriptController $@
