from prefect import flow
from tasks.transfermarkt import ingest_transfers_by_date
from redis import Redis
from datetime import datetime, timedelta
import json

redis = Redis(host='redis', port=6379, password='secret_redis')

@flow
def transfermarkt_incremental():

    last_ingestion_date = redis.get('transfermarkt_incremental.last_ingestion_date').decode('UTF-8') if redis.exists('transfermarkt_incremental.last_ingestion_date') else '2000-01-01'
    dt_last_ingestion_date = datetime.strptime(last_ingestion_date, '%Y-%m-%d')
    dt_current_ingestion_date = dt_last_ingestion_date + timedelta(days=1)
    current_ingestion_date = dt_current_ingestion_date.strftime('%Y-%m-%d')

    print(f"DEBUG - transfermarkt_incremental.py:transfermarkt_incremental() - current_ingestion_date: {current_ingestion_date}")
    transfers = ingest_transfers_by_date(current_ingestion_date)

    if (len(transfers)):
        y = dt_current_ingestion_date.strftime('%Y')
        m = dt_current_ingestion_date.strftime('%m')
        with open(f"/home/prefect/.prefect/transfers_by_day/y={y}/m={m}/transfers_by_day__{current_ingestion_date}.json", 'w') as f:
            f.write(json.dumps(transfers), indent=2)

    redis.set('transfermarkt_incremental.last_ingestion_date', current_ingestion_date)

if __name__ == '__main__':
    transfermarkt_incremental()