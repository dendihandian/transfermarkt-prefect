#!/bin/sh

prefect deployment apply deployments/first_flow__daily-deployment.yaml

prefect deployment set-schedule first-flow/first_flow__daily --cron '*/2 * * * *'

prefect agent start -q default