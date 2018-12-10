# Specify BROKER_URL and QUEUE when running
FROM ubuntu:14.04

RUN apt-get update && \
    apt-get install -y curl ca-certificates amqp-tools python \
       --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pika

COPY ./worker.py /worker.py

CMD  /worker.py
