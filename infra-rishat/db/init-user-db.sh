##!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail


psql -v ON_ERROR_STOP=1 --username "${POSTGRES_USER}" --dbname "${POSTGRES_DB}" <<-EOSQL
    CREATE DATABASE ${APP_DB_NAME};
    CREATE USER ${APP_DB_USER} WITH ENCRYPTED PASSWORD '${APP_DB_PASSWORD}';
    GRANT ALL PRIVILEGES ON DATABASE ${APP_DB_NAME} TO ${APP_DB_USER};
EOSQL

