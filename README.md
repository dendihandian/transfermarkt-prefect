# Transfermarkt Pipeline (Prefect)

![transfermarkt-prefect-architecture](/docs/images/transfermarkt-prefect-architecture.drawio.png)
## Requirements

- docker
- docker-compose

## How to run

minimal services for scheduled ingestion only:
```
docker compose up -d redis prefect-agent
```

all services:
```
docker compose up -d
```

## Services

### Prefect Agent

- prefect orchestrator to run and deploy the scheduled ingestion script.
- executing a flow manually example:

    ```
    docker-compose exec agent python src/flows/transfermarkt_incremental_page.py
    ```

### Prefect UI
- prefect web ui to monitor flow runs, enable/disable deployments, etc.
- access at [localhost:4200](http:/localhost:4200)

### Redis
- storage to save the ingestion bookmark and statuses.

### PHPRedisAdmin
- web ui to browse and manage redis keys and values.
- access at [localhost:9987](http:/localhost:9987)

### Jupyter Notebook
- jupyter notebook to process and analyzing data
- access at [localhost:8888](http:/localhost:8888?token=secret_token)

