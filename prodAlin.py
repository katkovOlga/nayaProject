from kafka import KafkaProducer
#while True:
par = "aspirin"
topic='GetDrug'
brokers = ['Cnt7-naya-cdh63:9092']
producer = KafkaProducer(bootstrap_servers=brokers)
#### Getting the data ready for kafka ####
producer.send(topic, value=par.encode('utf-8'))
producer.flush()