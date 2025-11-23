from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(bootstrap_servers='localhost:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

machines = ['Machine1', 'Machine2', 'Machine3']

while True:
    for machine in machines:
        data = {
            'machine': machine,
            'temperature': random.randint(60, 100),
            'status': 'OK'
        }
        producer.send('machines', value=data)
        print(f"Sent: {data}")
    time.sleep(5)
