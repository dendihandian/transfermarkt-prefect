from prefect import flow
from tasks.transfermarkt import ingest_transfers_by_date
from datetime import datetime, timedelta
import os
import pandas as pd

@flow
def transfermarkt_backfill():

    missing_dates = [
        # '2000-02-06',
        # '2000-02-07',
        # '2000-04-07',
        # '2000-05-10',
        # '2000-07-01',
        # '2000-07-06',
        # '2000-07-11',
        # '2000-07-13',
        # '2000-08-08',
        # '2000-08-09',
        # '2000-08-10',
        # '2000-09-29',
        # '2000-10-05',
        # '2000-10-13',
        # '2000-10-18',
        # '2000-11-09',
        # '2000-12-04',
        # '2001-01-11',
    ]

    for missing_date in missing_dates:

        transfers = ingest_transfers_by_date(missing_date)

        if (len(transfers)):

            filepath = f"/home/prefect/.prefect/transfers_by_day/"
            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            df = pd.DataFrame(transfers)
            df.to_parquet(filepath, partition_cols=['y', 'm', 'd'])

if __name__ == '__main__':
    transfermarkt_backfill()