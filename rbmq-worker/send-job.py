import pika
import os
import gridfs
import pymongo
import json

def connectToDB():
    client = pymongo.MongoClient('mongodb://'+os.environ['RABBITMQ_SERVER'])
    db = client.inputFiles
    collection = db.inputFiles
    fs = gridfs.GridFS(db)
    return db, collection, fs

def send_message(message_body):
    credentials = pika.PlainCredentials('srini', 'srini')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(os.environ['RABBITMQ_SERVER'], 5672, '/', credentials)
    )
    channel = connection.channel()

    channel.queue_declare(queue='tasks', durable=True)

    channel.basic_publish(exchange='',
                          routing_key='tasks',
                          body=message_body,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))

    print("[x] Message sent")

    connection.close()

# create job description send to queue
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

db, collection, fs = connectToDB()
file = fs.find_one({"filename": "input_script.py"})
if not file:
    f = open("./my-worker-script.py", "rb")
    fileID = fs.put(f, filename="input_script.py")
    print(fileID)

else:
    print("file already exists")


send_message(json.dumps(job))
