# !pip install TextBlob
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from textblob import TextBlob
from pyspark.sql.types import StringType, StructType, IntegerType, FloatType

# conection between  spark and kafka
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.1 pyspark-shell'

bootstrapServers = "Cnt7-naya-cdh63:9092"
def runConsumer(topic):

    spark = SparkSession\
        .builder\
        .appName("ReadInteraction")\
        .getOrCreate()

    # ReadStream from kafka
    df_kafka = spark\
        .readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", bootstrapServers)\
        .option("subscribe", topic)\
        .load()

    # Create schema for create df from json
    schema = StructType() \
        .add("DrugName", StringType()) \
        .add("drug_id", StringType()) \
        .add("description", StringType()) \
        .add("user_acount_created_at", StringType()) \
        .add("user_id", StringType())\
        .add("name", StringType()) \
        .add("followers_count", IntegerType()) \
        .add("friends_count", IntegerType())  \
        .add("listed_count", IntegerType())


    # change json to dataframe with schema
    df_inter = df_kafka.select(col("value").cast("string"))\
        .select(from_json(col("value"), schema).alias("value"))\
        .select("value.*")

    # Add current time in timestamp in column "current_ts"
    #df_tweets = df_tweets.withColumn("current_ts", current_timestamp().cast('string'))

    # Add hour current time  in column "hour"
    #df_tweets = df_tweets.withColumn("hour", hour("current_ts").cast('integer'))

    # Add minute current time in column "minute"
    #df_tweets = df_tweets.withColumn("minute", minute("current_ts").cast('integer'))

    # Add wordcount in column "wordCount"
    #df_tweets = df_tweets.withColumn('wordCount', size(split(col('text'), ' ')))

    # Filter just more than 10 words in tweets
    #df_tweets = df_tweets.where(col("wordCount") > 10)

    # Add sentiment analysis in column "wordCount"
    def get_sentiment(string1):
        return TextBlob(string1).sentiment.polarity

    get_sentiment_udf = udf(get_sentiment, FloatType())
    df_inter = df_inter.withColumn('sentiment', get_sentiment_udf(col('description')))

    df_inter \
        .writeStream \
        .format("console") \
        .start().stop()
        #.awaitTermination()
