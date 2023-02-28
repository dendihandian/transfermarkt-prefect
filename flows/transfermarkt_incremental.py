from prefect import flow, get_run_logger
from tasks.transfermarkt import ingest_transfers_by_date
from tasks.utils.transfermarkt import get_transfers_page_count_by_date
from redis import Redis
from datetime import datetime, timedelta
import json
import os
import pandas as pd

redis = Redis(host='redis', port=6379, password='secret_redis')

@flow
def transfermarkt_incremental():
    logger = get_run_logger()

    last_ingestion_date = redis.get('transfermarkt_incremental.last_ingestion_date').decode('UTF-8') if redis.exists('transfermarkt_incremental.last_ingestion_date') else '2010-01-01'
    dt_last_ingestion_date = datetime.strptime(last_ingestion_date, '%Y-%m-%d')
    dt_current_ingestion_date = dt_last_ingestion_date + timedelta(days=1)
    current_ingestion_date = dt_current_ingestion_date.strftime('%Y-%m-%d')

    if get_transfers_page_count_by_date(current_ingestion_date) <= 30:

        logger.info(f"DEBUG - flows/transfermarkt_incremental.py:transfermarkt_incremental() - current_ingestion_date: {current_ingestion_date}")
        transfers = ingest_transfers_by_date(current_ingestion_date)

        if (len(transfers)):

            filepath = f"/home/prefect/.prefect/transfers_by_day/"
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            df = pd.DataFrame(transfers)
            df.to_parquet(filepath, partition_cols=['y', 'm', 'd'])
    
    else:
        # TODO: find suitable redis data type to append a value to list (queue FIFO is better), and can be removed later.
        redis.set('transfermarkt_incremental.last_ingestion_date', current_ingestion_date)

    redis.set('transfermarkt_incremental.last_ingestion_date', current_ingestion_date)

if __name__ == '__main__':
    transfermarkt_incremental()