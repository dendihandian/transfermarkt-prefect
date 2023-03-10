FROM prefecthq/prefect:2.8.2-python3.10

WORKDIR /root

COPY ./init.sh ./init.sh
COPY ./src ./src

ENV PYTHONPATH=/root/src
ENV EXTRA_PIP_PACKAGES="pandas==1.5.3 beautifulsoup4==4.11.2"