import pika
import os
import time
import gridfs
import pymongo
import json
import importlib.util
from runpy import run_path

def load_local(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    my_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(my_module)
    return my_module

def connectToDB():
    client = pymongo.MongoClient('mongodb://'+os.environ['RABBITMQ_SERVER'])
    db = client.inputFiles
    collection = db.inputFiles
    fs = gridfs.GridFS(db)
    return db, collection, fs

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
    parsed_message = json.loads(message)

    db, collection, fs = connectToDB()
    file = fs.find_one({"filename": "input_script.py"})
    if file:
        # read the file from gridfs and do work
        worker = fs.get(file._id)
        f = open("temp-worker.py", "wb")
        f.write(worker.read())
        f.close()
        # once the temp file is created run the importlib.util.module_from_spec to run the script
        worker = load_local("my-worker", "./temp-worker.py")
        print(dir(worker))
        print(worker.__name__)
        print(worker.__loader__)
        print(worker.__package__)
        print(worker.__spec__)

def receive_message():
    credentials = pika.PlainCredentials('srini', 'srini')
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ['RABBITMQ_SERVER'], 5672, '/', credentials))
    channel = connection.channel()

    channel.queue_declare(queue='tasks', durable=True)

    def callback(ch, method, properties, body):
        print(" [x] Received ")
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
