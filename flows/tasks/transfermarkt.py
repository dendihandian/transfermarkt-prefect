from prefect import task, get_run_logger
from .utils.transfermarkt import get_transfers_by_date

@task
def ingest_transfers_by_date(date):

    logger = get_run_logger()

    transfers = get_transfers_by_date(date)
    logger.info(f"DEBUG - tasks/transfermarkt.py:ingest_transfers_by_date() - transfers count: {len(transfers)}")

    return transfers
