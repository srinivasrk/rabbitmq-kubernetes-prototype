# Specify BROKER_URL and QUEUE when running
FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y curl ca-certificates amqp-tools python python3-pip\
       --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pika

COPY ./worker.py /worker.py

RUN chmod +x /worker.py

CMD  /worker.py
