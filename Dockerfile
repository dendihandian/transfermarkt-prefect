FROM prefecthq/prefect:2.8.2-python3.10

RUN useradd -ms /bin/bash prefect

USER prefect

WORKDIR /home/prefect

COPY --chown=prefect:prefect requirements.txt requirements.txt
COPY --chown=prefect:prefect init.sh init.sh
COPY --chown=prefect:prefect ./flows/ ./flows/
COPY --chown=prefect:prefect ./tasks/ ./tasks/
COPY --chown=prefect:prefect ./utils/ ./utils/
COPY --chown=prefect:prefect ./deployments/ ./deployments/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
