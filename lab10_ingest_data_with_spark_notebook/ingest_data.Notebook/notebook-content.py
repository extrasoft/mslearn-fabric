# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "12118f82-246a-4077-84a5-892f328efa17",
# META       "default_lakehouse_name": "lab10_lakehouse",
# META       "default_lakehouse_workspace_id": "0723d55b-3a25-436f-9640-a2e8906ee30e",
# META       "known_lakehouses": [
# META         {
# META           "id": "12118f82-246a-4077-84a5-892f328efa17"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# ##### Create a Fabric notebook and load external data

# CELL ********************

# Azure Blob Storage access info
blob_account_name = "azureopendatastorage"
blob_container_name = "nyctlc"
blob_relative_path = "yellow"

# Construct connection path
wasbs_path = f'wasbs://{blob_container_name}@{blob_account_name}.blob.core.windows.net/{blob_relative_path}'
print(wasbs_path)

# Read parquet data from Azure Blob Storage path
blob_df = spark.read.parquet(wasbs_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(blob_df.count())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(blob_df.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Declare file name    
file_name = "yellow_taxi"
abfs_path = "abfss://lab10_ingest_data_with_spark_notebook@onelake.dfs.fabric.microsoft.com/lab10_lakehouse.Lakehouse/Files/RawData"
relative_path_for_spark = "Files/RawData"
file_api_path = "/lakehouse/default/Files/RawData"

# ABFS Path: abfss://lab10_ingest_data_with_spark_notebook@onelake.dfs.fabric.microsoft.com/lab10_lakehouse.Lakehouse/Files/RawData
# Relative path for Spark: Files/RawData
# File API path: /lakehouse/default/Files/RawData

# Construct destination path
output_parquet_path = f"abfss://lab10_ingest_data_with_spark_notebook@onelake.dfs.fabric.microsoft.com/lab10_lakehouse.Lakehouse/Files/RawData/{file_name}"
print(output_parquet_path)
    
# Load the first 1000 rows as a Parquet file
blob_df.limit(1000).write.mode("overwrite").parquet(output_parquet_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Transform and load data to a Delta table

# CELL ********************

from pyspark.sql.functions import col, to_timestamp, current_timestamp, year, month

# Read the parquet data from the specified path
raw_df = spark.read.parquet(output_parquet_path)   

# Add dataload_datetime column with current timestamp
filtered_df = raw_df.withColumn("dataload_datetime", current_timestamp())

# Filter columns to exclude any NULL values in storeAndFwdFlag
filtered_df = filtered_df.filter(col("storeAndFwdFlag").isNotNull())

# Load the filtered data into a Delta table
table_name = "yellow_taxi"
filtered_df.write.format("delta").mode("append").saveAsTable(table_name)

# Display results
display(filtered_df.limit(1))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### Analyze Delta table data with SQL queries

# CELL ********************

# Load table into df
delta_table_name = "yellow_taxi"
table_df = spark.read.format("delta").table(delta_table_name)

# Create temp SQL table
table_df.createOrReplaceTempView("yellow_taxi_temp")

# SQL Query
table_df = spark.sql('SELECT * FROM yellow_taxi_temp')

# Display 10 results
display(table_df.limit(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
