from confluent_kafka import Consumer


c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})

c.subscribe(['kafka_DLQ'])

while True:
    msg = c.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    print('Received value message: {}'.format(msg.value().decode('utf-8')))
    print('Received header message: {}'.format(msg.headers()))

c.close()

# except SerializerError as e:
# print("Message deserialization failed for {}: {}".format(msg, e))
# break
#
# if msg is None:
#     continue
#
# if msg.error():
#     print("AvroConsumer error: {}".format(msg.error()))
#     continue