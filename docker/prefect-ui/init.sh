#!/bin/bash

prefect config set PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://prefect:prefect@postgres:5432/prefect_db"

prefect server start --host 0.0.0.0 --port 4200