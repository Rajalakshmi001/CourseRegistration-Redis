import redis
import json
# import msgpack
from kafka import KafkaConsumer
db = None

def listen(consumer):
    for msg in consumer:
        data = json.loads(msg.content.decone('utf-8'))
        print(data)

if __name__ == '__main__':
    consumer = KafkaConsumer('redis', bootstrap_servers='137.112.89.91:9092', group_id='RedisReg', auto_offset_reset='latest')
    db = redis.StrictRedis(charset="utf-8", decode_responses=True)
    assert(db.ping() == True)

    listen(consumer)