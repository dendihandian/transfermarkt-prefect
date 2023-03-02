from prefect import flow, get_run_logger
from tasks.transfermarkt import ingest_transfers_by_date
from tasks.utils.transfermarkt import get_transfers_page_count_by_date
from redis import Redis
from datetime import datetime, timedelta
import json
import os
import pandas as pd

redis = Redis(host='redis', port=6379, password='secret_redis', charset="utf-8", decode_responses=True)

@flow
def transfermarkt_incremental():
    logger = get_run_logger()

    last_ingestion_date_key = 'transfermarkt_incremental:last_ingestion_date'
    last_ingestion_date = redis.get(last_ingestion_date_key) if redis.exists(last_ingestion_date_key) else '2010-01-01'
    dt_last_ingestion_date = datetime.strptime(last_ingestion_date, '%Y-%m-%d')
    dt_current_ingestion_date = dt_last_ingestion_date + timedelta(days=1)
    current_ingestion_date = dt_current_ingestion_date.strftime('%Y-%m-%d')

    total_page = get_transfers_page_count_by_date(current_ingestion_date)
    if total_page <= 30:

        logger.info(f"DEBUG - current_ingestion_date: {current_ingestion_date}")
        transfers = ingest_transfers_by_date(current_ingestion_date)

        if (len(transfers)):

            filepath = f"/home/prefect/.prefect/transfers_by_day/"
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            df = pd.DataFrame(transfers)
            df.to_parquet(filepath, partition_cols=['y', 'm', 'd'])
    
    else:
        redis.hset(f'transfermarkt_incremental_page:{current_ingestion_date}', 'status', 'ready')
        redis.hset(f'transfermarkt_incremental_page:{current_ingestion_date}', 'total_page', total_page)
        redis.hset(f'transfermarkt_incremental_page:{current_ingestion_date}', 'transfers_count', 0)
        redis.hset(f'transfermarkt_incremental_page:{current_ingestion_date}', 'last_ingestion_page', 0)

    redis.set(last_ingestion_date_key, current_ingestion_date)

if __name__ == '__main__':
    transfermarkt_incremental()