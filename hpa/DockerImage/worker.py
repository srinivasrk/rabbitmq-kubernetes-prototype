#!/usr/bin/env python3
import pika
import os
import time
import sys
import random
from flask import Flask
from flask_restful import Api, Resource, reqparse

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

    channel.queue_declare(queue=os.environ['QUEUE'], durable=True)
    print(" Worker Spwaning")
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        i = random.randint(100, 300) # generate a random number b/w 1000 and 9999
        for k in range(i):
            print(recur_fibo(k)) # find its Fibonacci
        time.sleep(2)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return 200

    # send ack
    channel.basic_consume(callback,
                          queue=os.environ['QUEUE'])

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


app = Flask(__name__)

@app.route('/')
def hello_world():
    print("Hello World : GET REQUEST RECEIVED")
    try:
        return receive_message()
        sys.exit()
    except:
        print("Error")
        sys.exit()



app.run(debug=True)