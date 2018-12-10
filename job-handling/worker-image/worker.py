#!/usr/bin/env python

# Just prints standard out and sleeps for 10 seconds.
import sys
import time
print("Processing " + sys.stdin.lines())
time.sleep(10)


import pika
import os
import time

def receive_message():
    credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['BROKER_URL'], 5672, '/', credentials))
    channel = connection.channel()

    channel.queue_declare(queue=os.environ['QUEUE'])

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        time.sleep(2)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # send ack
    channel.basic_consume(callback,
                          queue=os.environ['QUEUE'])

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


receive_message()
