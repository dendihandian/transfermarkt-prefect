from prefect import flow, get_run_logger
from tasks.transfermarkt import ingest_transfers_by_date_and_page
from redis import Redis
import os
import pandas as pd
import time

redis = Redis(host='redis', port=6379, password='secret_redis', charset="utf-8", decode_responses=True)

def get_current_key():

    keys = [key for key in redis.keys('transfermarkt_incremental_page:*')]

    current_key = None

    # check for progress available
    for key in keys:
        if redis.hget(key, 'status') == 'progress':
            current_key = key
            break

    # check for ready available
    if current_key == None:
        for key in keys:
            if redis.hget(key, 'status') == 'ready':
                current_key = key
                break

    return current_key

@flow
def transfermarkt_incremental_page():
    logger = get_run_logger()

    current_key = get_current_key()

    if (current_key):

        current_date = current_key.split(':')[-1]
        current_key_values = redis.hgetall(current_key)
        current_page = int(current_key_values['last_ingestion_page']) + 1

        transfers = ingest_transfers_by_date_and_page(current_date, current_page)

        if (len(transfers)):

            filepath = f"/home/prefect/.prefect/transfers_by_day/"
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            df = pd.DataFrame(transfers)
            df.to_parquet(filepath, partition_cols=['y', 'm', 'd'])

            redis.hset(current_key, 'status', 'progress')
            redis.hincrby(current_key, 'last_ingestion_page', 1)
            redis.hincrby(current_key, 'transfers_count', len(transfers))

        else:

            redis.hset(current_key, 'status', 'completed')

    else:
        print('all incremental page completed')


if __name__ == '__main__':
    transfermarkt_incremental_page()