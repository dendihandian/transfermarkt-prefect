#!/bin/bash

# if you're using windows, make sure this init.sh file encoded to LF instead of CRLF

prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://prefect:prefect@postgres:5432/prefect_db"

prefect agent start -q default