import pika
import pymongo
import sys

queue = sys.argv[1]

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["msgqueuedb"]
customers = db["msgqueue"]

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    customers.update_many({"queue": queue}, {"$set": {"status": 0}})


channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
