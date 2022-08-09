# UI  buttons functionality
#  written by Olga Katkov
import json
import configuration as c
import ProducerReq as pr
from kafka import KafkaConsumer
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from textblob import TextBlob
from pyspark.sql.types import StringType, StructType, IntegerType, FloatType
from multiprocessing import Pool
import asyncio

# conection between  spark and kafka
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.1 pyspark-shell'

def findPatient(tz):
    pass


def checkDrug(drugName):
    pr1 = pr.Producer()
    # async run to producer GetDrug
    # #  consumer to listen -- if exist previous  -- to use
    #

    asyncio.run((pr1.send(c.topic1, drugName.capitalize())))

    topic =c.topic2 + drugName.capitalize() #'GetInteractionaspirin'
    print (topic)
    spark = SparkSession \
        .builder \
        .appName("GetDrugInteraction") \
        .getOrCreate()
    # ReadStream from kafka

    df_kafka = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", c.brokers)\
        .option("subscribe", topic) \
        .option("includeHeaders", "true") \
        #.option("startingOffsets", "earliest") \
        .option("endingOffsets", "latest") \
        .load()


# Create schema for create df from json
schema = StructType() \
    .add("tweet_created_at", StringType()) \
    .add("tweet_id", StringType()) \
    .add("text", StringType()) \
    .add("user_acount_created_at", StringType()) \
    .add("user_id", StringType()) \
    .add("name", StringType()) \
    .add("followers_count", IntegerType()) \
    .add("friends_count", IntegerType()) \
    .add("listed_count", IntegerType())



     #return df


def createReceipt(self):
    pass


def addDiagnose(name):
    pass



#### function tests
checkDrug ('aspirin')