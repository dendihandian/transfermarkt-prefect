from prefect import task, flow
from datetime import datetime

@task
def first_task():
    print(f"first_task executed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@flow
def first_flow():
    print(f"first_flow running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    first_task()

if __name__ == '__main__':
    first_flow()
