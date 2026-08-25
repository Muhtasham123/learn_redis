import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))

channel = connection.channel()

channel.queue_declare('email_queue')

messages  = [
        {
        "to":"muhtasham@gmail.com",
        "subject":"Greeting",
        "body":"Hello there"
        },
        {
        "to":"bilal@gmail.com",
        "subject":"Greeting",
        "body":"Hello there"
        },
        {
        "to":"amna@gmail.com",
        "subject":"Greeting",
        "body":"Hello there"
        },
        {
        "to":"hina@gmail.com",
        "subject":"Greeting",
        "body":"Hello there"
        },
]

for message in messages:
    channel.basic_publish(
        exchange='',
        routing_key='email_queue',
        body=json.dumps(message)
    )

print("All Messages sent")
connection.close()