FROM python:3.10-slim

LABEL maintainer="dendihandian"

RUN useradd -ms /bin/bash prefect

USER prefect

WORKDIR /home/prefect

RUN pip install -U prefect

RUN export PATH="/home/prefect/.local/bin:$PATH"

COPY task.py /home/prefect/task.py

RUN touch /home/prefect/service.log

CMD tail -f /home/prefect/service.log