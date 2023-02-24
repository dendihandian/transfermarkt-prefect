FROM prefecthq/prefect:2.8.2-python3.10

RUN useradd -ms /bin/bash prefect

USER prefect

WORKDIR /home/prefect

COPY requirements.txt requirements.txt

COPY init.sh init.sh

COPY flows flows

RUN pip install --upgrade pip

RUN pip install -r requirements.txt
