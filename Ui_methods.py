# UI  buttons functionality
#  written by Olga Katkov
import json

import configuration as c
import ProducerReq as pr
from kafka import KafkaConsumer

import os
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StringType, StructType, IntegerType, FloatType
# from multiprocessing import Pool
# import asyncio
import pymongo

from  PatientClass import Patient
import pandas as pd
import pyarrow as pa
# conection between  spark and kafka
#os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.1 pyspark-shell'

def findPatient(tz):
    pat=Patient()
    pat.tz= tz
    pat.findPatient()
    return pat

#insert item to mongodb if not exist
def write_df_mongo(target_df):
    try:
        mogodb_client = pymongo.MongoClient('mongodb://localhost:27017/')
        mydb = mogodb_client["DrugInteraction"]
        mycol = mydb["Drugs"]

        print(target_df['MainDrugId'], target_df['MainDrugName'])
        if mycol.count_documents({"MainDrugId": target_df['MainDrugId']}, limit=1) == 0:

            post = {
                "MainDrugId": target_df['MainDrugId'],
                "MainDrugName": target_df['MainDrugName'],
                "DrugsIdList": target_df['DrugsIdList'],
                "drugNameList": target_df['drugNameList'],
                "severityList": target_df['severityList'],
                "descriptionList": target_df['descriptionList']
            }
            mycol.insert_one(post)
            print('item inserted to mango')
        else:
            # myquery = {"MainDrugId":target_df['MainDrugId'][0]}
            # newvalues = {"$set": {"DrugsIdList": target_df['DrugsIdList'],
            # "drugNameList": target_df['drugNameList'],
            # "severityList": target_df['severityList'],
            # "descriptionList": target_df['descriptionList']}}
            #
            # mycol.update_one(myquery, newvalues)

            print("already exist")

    except Exception as e:
        print(e)
# df_waiting_list \
#     .writeStream \
#     .foreach(write_df_mongo)\
#     .outputMode("append") \
#     .start() \
#     .awaitTermination()

def checkDrugKf(drugName,Pat1):
    try:
        pr1 = pr.Producer()
        lstSeverityUsedIter = []
        lstDescUsedIter = []
        topic = c.topic2 + drugName.capitalize()
        consumer = KafkaConsumer(topic, bootstrap_servers=c.bootstrapServers)
        pr1.send(c.topic1,drugName.capitalize())
        #print("before")
        for message in consumer:
            #print(message.value)
            valJson=json.loads(message.value)
            paDf=pd.json_normalize(valJson) #, record_path =['students'])
            #Medcine check interaction

            id= paDf['rxcui'][0]
            name=paDf['name'][0]
            #print(id,name)
            idList=[di for di in paDf['IdList'][0] if di != id]
            NameList=[ni for ni in paDf['NameList'][0] if ni != name]
            descLst=paDf['description'][0]
            severityList=[ClassifyDesc(desc) for desc in descLst]
            dictInterFull = {'MainDrugId':id,"MainDrugName":name,"DrugsIdList": idList,'drugNameList': NameList, 'severityList': severityList, 'descriptionList': descLst}
            write_df_mongo(dictInterFull)

            lstUsedInter=[el for  el in NameList if el in Pat1.ConstantDrugsList]
            lstIndexUsedIter=[NameList.index(el) for el in NameList if el in Pat1.ConstantDrugsList]
            if len(lstIndexUsedIter)>0:
               for i in  lstIndexUsedIter:
                  lstSeverityUsedIter.append(severityList[i])
                  lstDescUsedIter.append(descLst[i])

            #print (lstSeverityUsedIter,lstDescUsedIter)
            break
        dict = {'drug name': lstUsedInter, 'severity': lstSeverityUsedIter, 'description': lstDescUsedIter}
        resDf=pd.DataFrame(dict)
        # print (resDf)
        # print(id)
        return id,resDf
    except Exception as e:
        print(e)
        return pd.DataFrame()


def checkDrug(drugName,Pat1):
    pr1 = pr.Producer()
    # async run to producer GetDrug
    # #  consumer to listen -- if exist previous  -- to use
    #
    print(drugName.capitalize())
    os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.1 pyspark-shell'
    #asyncio.run(pr1.send(c.topic1, drugName.capitalize()))

    topic =c.topic2 + drugName.capitalize() #'GetInteractionaspirin'
    print (topic)
    spark = SparkSession \
        .builder \
        .appName("GetDrugInteraction") \
        .getOrCreate()
    # ReadStream from kafka
    #.option("startingOffsets", "earliest") \ spark.sqlContext.readStream
    # df_kafka = spark.readStream \
    #     .format("kafka") \
    #     .option("kafka.bootstrap.servers", c.bootstrapServers)\
    #     .option("subscribe", topic) \
    #     .option("includeHeaders", "true") \
    #     .option("endingOffsets", "latest") \
    #     .load()
    df_kafka = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", c.bootstrapServers)\
        .option("subscribe", topic) \
        .option("includeHeaders", "true") \
        .load()
    pr1.send(c.topic1, drugName.capitalize())
    # df_kafka = df_kafka.select(col("value").cast("string"))
    # print(df_kafka)
    # Create schema for create df from json
    #schema = StructType().add("name", StringType())         #     .add("rxcui", StringType()) \

    schema = StructType() \
        .add("rxcui", StringType()) \
        .add("name", StringType()) \
        .add("severity",StringType()) \
        .add("description",StringType()) \
        .add ("IdList",StringType()) \
        .add("NameList",StringType())
    # change json to dataframe with schema
    df_kafka.writeStream.format("console").start().awaitTermination()
    df1 = df_kafka.select(col("value").cast("string")) \
        .select(from_json(col("value"), schema).alias("value")) \
        .select("value.*")
    print('before 2')
    df1.writeStream.format("console").start().awaitTermination()

   # pr1.send(c.topic1, drugName.capitalize())

   #  print('after stream')
   #  paDf =df1.toPandas();
   #  print(paDf)
   #  #Medcine check interaction
   #  spark.stop()
   #  # exclude duplicates
   #  print(paDf['rxcui'])
   #  id= paDf['rxcui']
   #  name=paDf['name']
   #  idList=[di for di in paDf['IdList'].split(",") if di != id]
   #  NameList=[ni for ni in paDf['NameList'].split(",") if ni != name]
   # descLst=paDf['description'].split(",")
   #print (len(NameList), len(idList),len(descLst))
   #severityList=[ClassifyDesc(desc) for desc in paDf['description'].split('",')]
   # lstUsedInter =[el for  el in NameList if el in Pat1.ConstantDrugsList]
   # lstIndexUsedIter=[el.index() for el in NameList if el in Pat1.ConstantDrugsList]
   # lstSeverityUsedIter=[el for el in severityList if el.index() in lstIndexUsedIter]
   # lstDescUsedIter=[el for el in descLst if el.index() in lstIndexUsedIter]





     #return df


def createReceipt(self):
    pass


def addDiagnose(name):
    pass



def ClassifyDesc(desc):
    res=0
    if bool(re.search("adverse effects.*increased", desc)):
       res= -5
    elif bool(re.search("therapeutic efficacy.*increased", desc)):
        res=3
    elif bool(re.search("therapeutic efficacy.*decreased", desc)) :
        res=-2
    elif bool(re.search("risk or severity.*increased", desc)) :
        res=-4
    elif bool(re.search("excretion rate.*decreased", desc)):
        res=-1
    elif bool(re.search("metabolism.*increased", desc)) :
        res = 1
    elif bool(re.search("metabolism.*decreased", desc)) :
        res = -1
    elif bool(re.search("increase.*activities", desc)):
        res = 2
    elif bool(re.search("decrease.*activities", desc)):
        res = -2

    elif bool(re.search("decrease.*excretion rate", desc)):
        res = -1
    else:
        res=0
    #print (res)
    return res

#### function tests
#checkDrug ('aspirin')

pat1 =Patient()
pat1.TZ='889988998899'
df=pd.DataFrame()
id=""
pat1.findPatient()
id,df=checkDrugKf('rosuvastatin',pat1)
print(id,df)
#checkDrug('aspirin',pat1)

#
#r=ClassifyDesc('The therapeutic efficacy of Haloperidol can be increased when used in combination with Acetylsalicylic acid.')

