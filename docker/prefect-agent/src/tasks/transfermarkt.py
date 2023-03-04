from prefect import task, get_run_logger
from utils.transfermarkt import get_transfers_by_date, get_transfers_by_date_and_page

@task
def ingest_transfers_by_date(date):

    logger = get_run_logger()

    transfers = get_transfers_by_date(date)
    logger.info(f"DEBUG - current_date: {date}, transfers count: {len(transfers)}")

    return transfers

@task
def ingest_transfers_by_date_and_page(date, page):

    logger = get_run_logger()

    transfers = get_transfers_by_date_and_page(date, page)
    logger.info(f"DEBUG - current_date: {date}, page: {page}, transfers count: {len(transfers)}")

    return transfers
