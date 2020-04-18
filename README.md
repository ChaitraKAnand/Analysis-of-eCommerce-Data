# Analysis-of-eCommerce-Data
This repository consists of work done on analysis of eCommerce(Best Buy) data using Hadoop Components

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
* [Pipeline](#Pipeline)




<!-- ABOUT THE PROJECT -->
## About The Project

In the last few years, with the advancement of technologies and digitization, the amount of data generated rapidly increased from Terabytes to Zettabytes and by 2025, it is predicted there would a big and tremendous volume of data collections and that would be nearly 163 zettabytes. To handle this huge volume of data and process them to draw meaningful insights technologies like Hadoop and its ecosystem come to rescue.

To explore on big data technologies – Hadoop and its ecosystem, we opted to work on e-commerce data (Best Buy store website - "https://api.bestbuy.com/v1/").Data collected includes information on products such as Cell phones, Desktops and Laptops. We aim to store and analyse this data to draw useful insights such as compare price of different cell phones along with the carrier. On the same lines, compare cost of laptops across different brands. Customer top rated products and so on.


### Built With
Below are the technologies used to accomplish this project

1. Two node cluster of Google compute engine - CentOS 6(each 8vCPU's, 32GB RAM)
2. HDP -2.6 installed on 2 node cluster using Ambari
3. MongoDB - 3.2

<!-- GETTING STARTED -->
## Getting Started

Refer to the video to create Google cloud account and build two node cluster compute engine and install HDP -2.6 on it
https://www.youtube.com/watch?v=tCxY8UwcPXs&t=12s

To install MongoDB refer to "https://github.com/nikunjness/mongo-ambari" 

## Proposed pipeline

### Data Acquisition 

Refer script data_acquisition to pull the data using Best Buy REST API. Add API Key in the URL.

### Data Ingestion using Flume

Confiugure Flume configuration file by specifying Source ,channel and Sink. 

Confiuguration file

```python
#Source
bbagent.sources=restdata
bbagent.sources.restdata.channels=memoryChannel
bbagent.sources.restdata.handler=org.apache.flume.sink.solr.morphline.JSONHandler
bbagent.sources.restdata.port=5140
bbagent.sources.restdata.type=http

#Memory Channel 
bbagent.channels=memoryChannel
bbagent.channels.memoryChannel.capacity=100000
bbagent.channels.memoryChannel.transactionCapacity=100
bbagent.channels.memoryChannel.type=memory

#Sink
bbagent.sinks=tohdfs
bbagent.sinks.tohdfs.channel=memoryChannel
bbagent.sinks.tohdfs.hdfs.filePrefix=products-
bbagent.sinks.tohdfs.hdfs.fileType=DataStream
bbagent.sinks.tohdfs.hdfs.path=/user/flume/BestBuyData/
bbagent.sinks.tohdfs.hdfs.writeFormat=Text
bbagent.sinks.tohdfs.type=hdfs
```
### Data load on to mongoDB 

Data on HDFS is loaded on to MongoDB using "mongoimport"

hdfs fs -text /user/flume/BestBuyData/products-* | mongoimport --db db_name --collection collection_name

### ETL - Apache Spark and Hive

```python
 pyspark --jars "/root/mongo-hadoop-spark-2.0.2.jar"  --driver-class-path "/root/mongo-java-driver-3.4.2.jar" --py-files "/root/mongo-hadoop/spark/src/main/python/pymongo_spark.py" --packages org.mongodb.spark:mongo-spark-connector_2.11:2.2.7

from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession,HiveContext
from pyspark.sql.functions import col,explode

conf = SparkConf().set("spark.jars.packages","org.mongodb.spark:mongo-spark-connector_2.11:2.2.7")


spark = SparkSession\
.builder.\
appName("BestBuySpark")\
.config("spark.mongodb.input.uri", "mongodb://127.0.0.1/BestBuy.celphones")\
.config("spark.sql.warehouse.dir", "/root/spark-warehouse")\
.enableHiveSupport()\
.getOrCreate()

sqlContext = SQLContext(spark.sparkContext)

df = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri","mongodb://localhost/BestBuy.celphones").load()

 df.printSchema()


#Explode to convert array of struct into array of struct with rows and struct_columns

def flatten_struct_cols(df):
    flat_cols = [column[0] for column in df.dtypes if 'struct' not in column[1][:6]]
    struct_columns = [column[0] for column in df.dtypes if 'struct' in column[1][:6]]
    df = df.select(flat_cols +
                   [col(sc + '.' + c).alias(sc + '_' + c)
                   for sc in struct_columns
                   for c in df.select(sc + '.*').columns])
    return df

df = df.withColumn('products', explode(col('products')))
df = flatten_struct_cols(df)
df.printSchema()

#Create table from DataFrame 

df.registerTempTable('celphone_table')
sqlContext.sql('select * from celphone_table').show()

#Database on Hive
spark.sql("create database BestBuy")
DataFrame[]

sqlContext.sql("create table BestBuy.Cellphones as select  from celphone_table");


#Average cost of a celphone
AvgPrice = df.groupby("products_name").avg("products_regularPrice").collect()
type(AvgPrice)
AvgPrice = spark.createDataFrame(AvgPrice)
type(AvgPrice)
AvgPrice.registerTempTable('CellphoneAvgPrice')
AvgPrice = AvgPrice.withColumnRenamed("products_name","Name")
AvgPrice = AvgPrice.withColumnRenamed("avg(products_regularPrice)","AveragePrice")
AvgPrice.write.mode("overwrite").saveAsTable("BestBuy.CellphoneAvgPrice")

#Total review count for each celphone
reviewcount = sorted(df.groupBy(['products_name', df.products_customerReviewCount]).count().collect())
reviewcount = spark.createDataFrame(reviewcount)
reviewcount.write.mode("overwrite").saveAsTable("BestBuy.CellphoneReviewCount")
sqlContext.sql('select *  from CellphonesReviewCount').show()


#Data for laptops
laptops = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri","mongodb://localhost/BestBuy.laptops").load()
laptops = laptops.withColumn('products', explode(col('products')))
laptops = flatten_struct_cols(laptops)
AvgScreenSize = laptops.groupby("products_manufacturer").avg("products_screenSizeIn").collect()
AvgScreenSize = spark.createDataFrame(AvgScreenSize)
AvgScreenSize.registerTempTable('AvgScreenSize')
sqlContext.sql('select * from AvgScreenSize').show()
AvgScreenSize = AvgScreenSize.withColumnRenamed("products_manufacturer","manufacturer")
AvgScreenSize = AvgScreenSize.withColumnRenamed("avg(products_screenSizeIn)","AverageScreenSizeInches")
AvgScreenSize.write.mode("overwrite").saveAsTable("BestBuy.AvgScreenSize")

#Desktops 
desktops = sqlContext.read.format("com.mongodb.spark.sql.DefaultSource").option("uri","mongodb://localhost/BestBuy.desktops").load()
desktops = desktops.withColumn('products', explode(col('products')))
desktops = flatten_struct_cols(desktops)
MinSalePrice = laptops.groupby("products_modelNumber","products_manufacturer").min("products_salePrice").collect()
MinSalePrice = spark.createDataFrame(MinSalePrice)
MinSalePrice.registerTempTable('MinSalePrice')
sqlContext.sql('select * from MinSalePrice').show()
MinSalePrice = MinSalePrice.withColumnRenamed("min(products_salePrice)","MinSalePrice")
MinSalePrice.write.mode("overwrite").saveAsTable("BestBuy.MinSalePrice")

```

### Visualization using Apache Zeppelin

Access Zeppelin Web UI on port localhost:9995 and configure to access JDBC interpreter . Access hive "%hive" to visualize the data

