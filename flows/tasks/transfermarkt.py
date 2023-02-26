from prefect import task
from .utils.transfermarkt import get_transfers_by_date

@task
def ingest_transfers_by_date(date):

    transfers = get_transfers_by_date(date)

    print(f"transfers count: {len(transfers)}")
    return transfers
