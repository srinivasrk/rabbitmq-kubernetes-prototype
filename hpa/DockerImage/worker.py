#!/usr/bin/env python3
import pika
import os
import time
import sys
import random
from flask import Flask
from flask_restful import Api, Resource, reqparse

import logging
logger = logging.getLogger('hpa-custom')
hdlr = logging.FileHandler('/hpa-custom.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)


def recur_fibo(n):
   """Recursive function to
   print Fibonacci sequence"""
   if n <= 1:
       return n
   else:
       return(recur_fibo(n-1) + recur_fibo(n-2))


def receive_message():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq-service", 5672, '/', credentials))
    channel = connection.channel()

    channel.queue_declare(queue='hpa-custom', durable=True)
    print("Worker Spwaning")
    logger.info('Worker Spwaning')

    def callback(ch, method, properties, body):
        logger.info('Reading message')
        print(" [x] Received %r" % body)
        i = random.randint(100, 300)  # generate a random number b/w 1000 and 9999
        # for k in range(i):
        #     print(recur_fibo(k))  # find its Fibonacci
        # time.sleep(2)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return "done"

    # send ack
    channel.basic_consume(callback,
                          queue='hpa-custom')

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


app = Flask(__name__)

@app.route('/')
def hello_world():
    try:
        logger.info('received get request')
        receive_message()
        return "Done"
    except:
        e = sys.exc_info()[0]
        print(e)
        print("Error")
        sys.exit()

app.run(debug=True)