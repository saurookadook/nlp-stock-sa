SELECT
    'CREATE DATABASE the_money_maker'
WHERE
    NOT EXISTS (
        SELECT
        FROM
            pg_database
        WHERE
            datname = 'the_money_maker') \gexec

DO $body$
BEGIN
    IF NOT EXISTS (
        SELECT
            *
        FROM
            pg_user
        WHERE
            usename = 'app') THEN
        CREATE USER app WITH INHERIT LOGIN PASSWORD 'app';
    END IF;

    IF NOT EXISTS (
        SELECT
            *
        FROM
            pg_user
        WHERE
            usename = 'migrations') THEN
        CREATE USER migrations WITH INHERIT LOGIN PASSWORD 'migrations';
    END IF;
END
$body$;


ALTER DEFAULT PRIVILEGES GRANT USAGE ON SCHEMAS TO PUBLIC;


ALTER DEFAULT PRIVILEGES
FOR ROLE migrations GRANT
SELECT ON TABLES TO PUBLIC;


GRANT ALL ON SCHEMA public TO migrations;


REVOKE CREATE ON SCHEMA public FROM app;


ALTER DEFAULT PRIVILEGES
FOR ROLE migrations GRANT ALL ON TYPES TO app;


ALTER DEFAULT PRIVILEGES
FOR ROLE migrations GRANT ALL ON SEQUENCES TO app;


ALTER DEFAULT PRIVILEGES
FOR ROLE migrations GRANT INSERT, UPDATE, DELETE,
REFERENCES ON TABLES TO app;

