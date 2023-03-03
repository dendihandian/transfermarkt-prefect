from prefect import flow
from tasks.transfermarkt import ingest_transfers_by_date
from datetime import datetime, timedelta
import os
import pandas as pd
from redis import Redis

redis = Redis(host='redis', port=6379, password='secret_redis', charset="utf-8", decode_responses=True)

@flow
def transfermarkt_backfill():

    missing_date = redis.rpop('transfermarkt_backfill.queue')

    try:

        transfers = ingest_transfers_by_date(missing_date)

        if (len(transfers)):

            filepath = f"/home/prefect/.prefect/transfers_by_day/"
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            df = pd.DataFrame(transfers)
            df.to_parquet(filepath, partition_cols=['y', 'm', 'd'])

            redis.lpush('transfermarkt_backfill.queue_history', missing_date)

    except Exception as e:
        redis.rpush('transfermarkt_backfill.queue', missing_date)

if __name__ == '__main__':
    transfermarkt_backfill()