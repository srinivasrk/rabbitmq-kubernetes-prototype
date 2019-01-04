#!/usr/bin/env python
import pika
import uuid

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        print(body)

    def call(self, n):
        self.response = None
        self.channel.basic_publish(exchange='',
                                   routing_key='rpc_queue',
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue
                                         ),
                                   body=str(n))


fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
fibonacci_rpc.call(30)
fibonacci_rpc.call(10)
fibonacci_rpc.call(5)