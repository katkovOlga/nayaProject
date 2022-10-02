#  created by Olga Katkov  20/09/22
#  create reports from HDFS Archive by using spark
#  use udf for analysis of nested json df

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StringType, StructType, IntegerType, FloatType
import configuration as c
import os


def getCriticalRiskByKH():
    #os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.1 pyspark-shell'
    spark = SparkSession \
        .builder \
        .appName("ReportCriticalRiskByKH") \
        .getOrCreate()
    df = spark.read.json('hdfs://Cnt7-naya-cdh63:8020/user/alin/niv/data/')
    df = spark.read.json(c.hdfs_json_path)
    df.show(6, False)


    df.select(F.to_json(F.struct([F.col(c).alias(c) for c in df.columns])).alias('value')) \
            .writeStream.format("console").start().awaitTermination()

        #.save()
