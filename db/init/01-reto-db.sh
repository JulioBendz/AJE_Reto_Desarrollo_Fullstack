#!/bin/bash
set -euo pipefail

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<'EOSQL'
CREATE DATABASE "retoDB";
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "retoDB" <<'EOSQL'
CREATE TABLE cliente (
    id INTEGER PRIMARY KEY,
    nombres VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    telefono VARCHAR(50),
    fecha_creacion TIMESTAMP NOT NULL,
    estado INTEGER NOT NULL
);
EOSQL
