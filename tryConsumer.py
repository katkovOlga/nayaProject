from kafka import KafkaConsumer

# In this example we will illustrate a simple producer-consumer integration

topic1 = 'GetInteractionaspirin'
brokers = ['cnt7-naya-cdh63:9092']

# First we set the consumer,
# and we use the KafkaConsumer class to create a generator of the messages.

consumer = KafkaConsumer(topic1,bootstrap_servers=brokers)

# print the value of the consumer
# we run the consumer generator to fetch the message scoming from topic1.
for message in consumer:
    print(str(message.value))