DROP DATABASE IF EXISTS test_the_money_maker;


CREATE DATABASE test_the_money_maker ENCODING 'UTF8';

DO $body$
BEGIN
    IF NOT EXISTS (
        SELECT *
        FROM pg_user
        WHERE usename = 'app')
        THEN
        CREATE USER app WITH INHERIT LOGIN PASSWORD 'app';
    END IF;
END
$body$;

GRANT ALL ON SCHEMA public TO app;

