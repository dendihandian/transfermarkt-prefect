#!/bin/sh

prefect work-queue set-concurrency-limit default 1
prefect deployment apply deployments/transfermarkt_incremental__everyFiveMinute.yaml
prefect deployment set-schedule transfermarkt_incremental/everyFiveMinute --cron '*/5 * * * *'

prefect agent start -q default