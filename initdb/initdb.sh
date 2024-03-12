#!/bin/bash
set -e
export POSTGRES_PASSWORD=$POSTGRES_PASSWORD;
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" <<-EOSQL
  CREATE USER $APP_DB_USER WITH PASSWORD '$APP_DB_PASSWORD';
  CREATE DATABASE $APP_DB_NAME;
  GRANT ALL PRIVILEGES ON DATABASE $APP_DB_NAME TO $APP_DB_USER;
  \connect $APP_DB_NAME $APP_DB_USER
  BEGIN;
    CREATE TABLE IF NOT EXISTS event (
      id CHAR(26) NOT NULL CHECK (CHAR_LENGTH(id) = 26) PRIMARY KEY,
	    aggregate_id CHAR(26) NOT NULL CHECK (CHAR_LENGTH(aggregate_id) = 26),
	    event_data JSON NOT NULL,
	    version INT,
	    UNIQUE(aggregate_id, version)
    );
    CREATE INDEX idx_event_aggregate_id ON event (aggregate_id);
  COMMIT;
EOSQL
