#!/usr/bin/env python
import pika
import uuid
import os

class FibonacciRpcClient(object):
    def __init__(self):
        credentials = pika.PlainCredentials('srini', 'srini')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_SERVER'], 5672,
                                                                       '/', credentials))


        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        print(body)

    def call(self, n):
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to=self.callback_queue
                                         ),
                                   body=str(n))


fibonacci_rpc = FibonacciRpcClient()

fibonacci_rpc.call(30)
fibonacci_rpc.call(10)
fibonacci_rpc.call(5)
fibonacci_rpc.channel.start_consuming()