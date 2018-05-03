import redis
from kafka import KafkaConsumer
db = None

def listen(consumer):
    for msg in consumer:
        print(msg)

if __name__ == '__main__':
    consumer = KafkaConsumer('redis', bootstrap_servers='137.112.89.91:9092', group_id='RedisReg', auto_offset_reset='latest')
    db = redis.StrictRedis(charset="utf-8", decode_responses=True)
    print(db.ping())
    listen(consumer)