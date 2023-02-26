from prefect import task, flow
from datetime import datetime
from random import randint
from time import sleep
import logging

logging.basicConfig(level=logging.DEBUG)

@task
def first_task():
    logging.info(f"logging.info: first_task started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"first_task started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    sleep(randint(1, 10))
    logging.info(f"logging.info: first_task finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"first_task finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@flow
def first_flow():
    logging.info(f"logging.info: first_flow running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"first_flow running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    first_task()

if __name__ == '__main__':
    first_flow()
