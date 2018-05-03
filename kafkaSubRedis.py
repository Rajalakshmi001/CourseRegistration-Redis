import redis
import json
# import msgpack
from kafka import KafkaConsumer
from courses import *

db = None
topic = 'redis'

def listen(consumer):
    print("Subscribed to Kafka topic: " + topic)
    for msg in consumer:
        try:
            if msg.value is None:
                print("BAD MESSAGE: ", msg)
                continue
            payload = msg.value
            category = payload['category']
            data = payload['data']
            cmd = payload['command']
            
            if category == 'COURSE':
                course_handler(cmd, data)
            elif category == 'OFFERING':
                offering_handler(cmd, data)
        except Exception as e:
            print(e)

def course_handler(cmd, data):
    if cmd == 'CREATE':
        course_create(db, data)
    elif cmd == 'DELETE':
        course_delete(db, data)

def offering_handler(cmd, data):
    print(cmd, " > ", data)

def decode_message(m):
    try:
        return json.loads(m.decode('utf-8'))
    except:
        return None


if __name__ == '__main__':
    consumer = KafkaConsumer(topic, 
    bootstrap_servers='137.112.89.91:9092',
        #group_id='RedisReg', 
        group_id=None,
        auto_offset_reset = 'earliest',
        value_deserializer = decode_message
        )
    db = redis.StrictRedis(charset="utf-8", decode_responses=True)
    assert(db.ping() == True)
    print("Connected to Redis")
    listen(consumer)