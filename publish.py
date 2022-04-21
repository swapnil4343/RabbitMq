import pika
import pymongo
import sys

queue = sys.argv[1]
body = sys.argv[2]

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["msgqueuedb"]
customers = db["msgqueue"]

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue)
    channel.basic_publish(exchange='', routing_key=queue, body=body)
    x = customers.insert_one({"queue": queue, "msg": body, "status": 1})
    print(" [x] Sent 'Hello RabbitMQ!'")
    connection.close()

except Exception as e:
    print(str(e))
    x = customers.insert_one({"queue": queue, "msg": body, "status": 2})
