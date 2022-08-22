# ========================================================================================================= #
# ========================================Kafka Connections =============================================== #
# ========================================================================================================= #
bootstrapServers = "cnt7-naya-cdh63:9092"
topic1 = 'GetDrug'
topic2 = 'GetInteraction'




# ======== Format DataFrame to json file and Write it to HDFS  ==================== #
hdfs_json_path = 'hdfs://Cnt7-naya-cdh63:8020/user/naya/de_proj/hdfsarchive/'
hdfs_json_checkpoint_path = 'hdfs://Cnt7-naya-cdh63:8020/user/nay/de_proj/hdfsarchive.checkpoint/'

# ======== Format DataFrame to parquet file and Write it to HDFS  ==================== #
From_Kafka_To_Hdfs_Parquet_path = "hdfs://Cnt7-naya-cdh63:8020/user/alin/de_proj/traffic_parquet/"
From_Kafka_To_Hdfs_parquet_path_checkpointLocation = "hdfs://Cnt7-naya-cdh63:8020/user/alin/de_proj/traffic_parque.checkpoint/"
# ========================================================================================================= #
# =================================sql stocks connection =============================================== #
# ========================================================================================================= #
mysql_host = 'localhost'
mysql_port = 3306
mysql_database_name = "doctors"#'DIASESES'
mysql_username = 'naya'
mysql_password = 'NayaPass1!'
mysql_table_name = "patients" #'DiseasesFile'

# ========================================================================================================= #
# =================================/hive/ =============================================== #
host='Cnt7-naya-cdh63'
port=8020
user='hdfs'

hdfs_host = 'Cnt7-naya-cdh63'
hdfs_owner ='hdfs'
hdfs_group='supergroup'
source_path = '/user/naya/de_proj/traffic_parquet'
# ====== Settings to HUE Connection ===================== #
hue_port = 8889
hue_username = 'hdfs'
hue_password = 'naya'
# ====== Settings to Hive Connection ===================== #
hdfs_host = 'Cnt7-naya-cdh63'
hdfs_port = 9870
hive_port = 10000
hive_username = 'hdfs'
hive_password = 'naya'
hive_mode = 'CUSTOM'
hive_database= 'receipts_db'
# ====== Settings to impala Connection ===================== #
impala_host = 'Cnt7-naya-cdh63'
impala_port = 21050
impala_database = 'receipts_db'
impala_username = 'hdfs'
impala_password = 'naya'



