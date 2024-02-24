export DATABASE_NAME="the_money_maker"
export PSQL_CONNECTION="postgresql://postgres:example@database"

psql $PSQL_CONNECTION -c DROP DATABASE IF EXISTS $DATABASE_NAME
psql $PSQL_CONNECTION -f ./db/init_db.sql
