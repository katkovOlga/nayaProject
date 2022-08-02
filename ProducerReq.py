import json
import configuration as c

from kafka import KafkaProducer
from time import sleep


 #  {"DrugName":"Aspirin"}
#topic1 = 'GetDrug'
#brokers = ['cnt7-naya-cdh63:9092']




class Producer():
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=c.bootstrapServers)
        # self.request = []

    def send(self, topic,req):
        # data is the full *tweet* json data
         #api_req = json.loads(req)
         # send data to kafka topic(s)

        # print(type(  bytes(req, 'utf-8')))
        # breq=bytes(req, 'utf-8')
        #print (type (b'nana'))
        self.producer.send(topic, value=req.encode('utf-8') )
        #self.producer.send(topic, value=breq)
        #self.producer.send(topic, value=b'Ketoprofen')
        self.producer.flush()




    def on_error(self, status_code):
        if status_code == 420:
            return False



pr1=Producer()
#pr1.send("GetDrug" ,"""{"DrugName":"Aspirin"}""")

pr1.send(c.topic1,'Optalgin')


