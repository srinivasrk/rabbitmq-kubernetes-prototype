#!/usr/bin/env python3

import pika
import os
import time
import sys

def receive_message():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq-service", 5672, '/', credentials))
    channel = connection.channel()

    channel.queue_declare(queue=os.environ['QUEUE'], durable=True)
    print(" Worker Spwaning")
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        time.sleep(2)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        sys.exit()

    # send ack
    channel.basic_consume(callback,
                          queue=os.environ['QUEUE'])

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


receive_message()
