from prefect import task, flow

@task
def first_task():
    print('doing first_task')

@flow
def first_flow():
    print('first_flow running')
    first_task()

if __name__ == '__main__':
    first_flow()
