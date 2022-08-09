import json
import configuration as c
import ProducerReq as pr
from kafka import KafkaConsumer
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from textblob import TextBlob
from pyspark.sql.types import StringType, StructType, IntegerType, FloatType


# conection between  spark and kafka
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.1 pyspark-shell'

def findPatient(tz):
    pass


def checkDrug(drugName):
    pr1 = pr.Producer()
    # #pr1.send("GetDrug" ,"""{"DrugName":"Aspirin"}""")
    # #  consumer to listen -- exit funct
    # async run to producer GetDrug
    pr1.send(c.topic1,drugName.capitalize())


    # In this example we will illustrate a simple producer-consumer integration

    topic =c.topic2 + drugName.capitalize() #'GetInteractionaspirin'
    print (topic)

    # First we set the consumer,
    # and we use the KafkaConsumer class to create a generator of the messages.

    consumer = KafkaConsumer(topic, bootstrap_servers=c.brokers)

    # print the value of the consumer
    # we run the consumer generator to fetch the message scoming from topic1.
    for message in consumer:
        print(str(message.value))
     #return df



def createReceipt(self):
    pass


def addDiagnose(name):
    pass