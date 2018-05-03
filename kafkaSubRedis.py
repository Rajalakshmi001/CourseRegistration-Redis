import redis
import json
# import msgpack
from kafka import KafkaConsumer
db = None

def listen(consumer):
    for msg in consumer:
        print(msg.value)

if __name__ == '__main__':
    consumer = KafkaConsumer('redis', 
    bootstrap_servers='137.112.89.91:9092',
     group_id='RedisReg', 
        auto_offset_reset='latest',
        value_deserializer= lambda m: json.loads(m.decode('utf-8')))
    db = redis.StrictRedis(host='137.112.89.91', port='9092', charset="utf-8", decode_responses=True)
    assert(db.ping() == True)

    listen(consumer)