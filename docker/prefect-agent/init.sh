#!/bin/sh

prefect work-pool set-concurrency-limit default-agent-pool 1
prefect concurrency-limit create one-at-time 1

prefect deployment apply src/deployments/transfermarkt_incremental__everyMinute.yaml
prefect deployment apply src/deployments/transfermarkt_incremental_page__everyFifteenMinute.yaml

prefect deployment set-schedule transfermarkt-incremental/everyMinute --cron '* * * * *'
prefect deployment set-schedule transfermarkt-incremental-page/everyFifteenMinute --cron '*/15 * * * *'

prefect agent start -q default