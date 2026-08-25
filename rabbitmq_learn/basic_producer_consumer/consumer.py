import pika
import json
import random

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare('email_queue')

def consume_message(ch, method, properties, body):
    message = json.loads(body)

    print(f"Procesing message for {message["to"]}")
    print(f"Sebject : {message["subject"]}")

    if random.random() < 0.5:
        print("Worker CRASHD!!!!")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        return

    # Send message here in production
    ch.basic_ack(delivery_tag=method.delivery_tag)

    print("Done!")

channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='email_queue', on_message_callback=consume_message)

print("Waiting for message....")
channel.start_consuming()