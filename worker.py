from rq import Queue
from redis import Redis
from analyzer import sentiment_analysis
import pika
import config
import json

# import shared config
f = file('config.conf')
cfg = config.Config(f)

# Rabbit channel listener
connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg.sentiment.RABBIT_HOST))
channel = connection.channel()
channel.queue_declare(queue=cfg.sentiment.QUEUE_TOPIC)

# Tell RQ what Redis connection to use
redis_conn = Redis()
q = Queue(connection=redis_conn)


def callback(ch, method, properties, body):
    decoded = json.loads(body)
    print(" [x] Received %r" % body)

    # text of the tweet in 'text' key
    if 'text' not in decoded:
        print(" [-] Invalid JSON")
    else:
        # Valid json

        ch.basic_ack(delivery_tag = method.delivery_tag)

        # start the job without waiting the response
        q.enqueue(sentiment_analysis, body)

        print(" [x] Done")


if __name__ == "__main__":
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue=cfg.sentiment.QUEUE_TOPIC, no_ack=False)
    channel.start_consuming()