#!/bin/sh

prefect work-pool set-concurrency-limit default-agent-pool 1
prefect work-queue set-concurrency-limit default 1

prefect deployment apply deployments/transfermarkt_incremental__everyFiveMinute.yaml
prefect deployment apply deployments/transfermarkt_incremental_page__everyFiveMinute.yaml

prefect deployment set-schedule transfermarkt-incremental/everyFiveMinute --cron '*/5 * * * *'
prefect deployment set-schedule transfermarkt-incremental-page/everyFiveMinute --cron '*/5 * * * *'

prefect agent start -q default