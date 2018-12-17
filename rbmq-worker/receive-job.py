import pika
import os
import time


def do_work(message):
    # the message is of the form
    '''
    job = {
        'type': 'analysis',
        'files': [
            {'name': 'sample.csv', 'path': 'sample_file.csv'}
        ],
        'run': './my-worker-script.py',
        'hooks': [
            'my-hook1.py',
            'my-hook2.py'
        ],
        'requester': '198e40e9-b822-4004-bb28-27efe573f23d',
        'parameters': {
            # some specifics for subtasks
        }
    }
    '''


def receive_message():
    credentials = pika.PlainCredentials('srini', 'srini')
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_SERVER'], 5672, '/', credentials))
    channel = connection.channel()

    channel.queue_declare(queue='tasks', durable=True)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
        do_work(body)
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Fair dispatch
    channel.basic_qos(prefetch_count=1)

    # send ack
    channel.basic_consume(callback,
                          queue='tasks')

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


receive_message()
