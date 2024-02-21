import asyncio
import os
import random
import sys
from datetime import datetime

from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from models import Purchase

BROKER_URL = os.environ["BROKER_URL"]
TOPIC_NAME = os.environ["TOPIC_NAME"]


def delivery_callback(err, msg):
    if err:
        sys.stderr.write(
            "%% %s: Message failed delivery: %s\n" % (datetime.now().isoformat(), err)
        )
    else:
        sys.stderr.write(
            "%% %s: Message delivered to %s \n"
            % (datetime.now().isoformat(), msg.topic())
        )


async def producer(topic_name):
    conf = {"bootstrap.servers": BROKER_URL}
    p = Producer(**conf)
    while True:
        p.produce(topic_name, Purchase().serialize(), callback=delivery_callback)
        p.poll(0)

        # Send Data at irregular times
        await asyncio.sleep(random.uniform(0.1, 1.0))


async def produce():
    t1 = asyncio.create_task(producer(TOPIC_NAME))
    await t1


def topic_exists(client, topic_name):
    topic_metadata = client.list_topics(timeout=5)
    return topic_metadata.topics.get(topic_name) is not None


def main():
    client = AdminClient({"bootstrap.servers": BROKER_URL})
    topic = NewTopic(TOPIC_NAME, num_partitions=2, replication_factor=1)

    if not topic_exists(client, TOPIC_NAME):
        client.create_topics([topic])

    try:
        asyncio.run(produce())
    except KeyboardInterrupt as e:
        print(f"shutting down, {e}")
    finally:
        client.delete_topics([topic])


if __name__ == "__main__":
    main()
