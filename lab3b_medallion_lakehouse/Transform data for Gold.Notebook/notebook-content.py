# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "95f37fb9-6965-4893-91c0-4e7db86dd5e6",
# META       "default_lakehouse_name": "Sales",
# META       "default_lakehouse_workspace_id": "aee5a40c-93d1-4697-b4f7-978a970a6b20",
# META       "known_lakehouses": [
# META         {
# META           "id": "95f37fb9-6965-4893-91c0-4e7db86dd5e6"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Load data to the dataframe as a starting point to create the gold layer
df = spark.read.table("Sales.sales_silver")

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 4. Create a dimdate_gold table

# CELL ********************

from pyspark.sql.types import *
from delta.tables import*
    
# Define the schema for the dimdate_gold table
DeltaTable.createIfNotExists(spark) \
    .tableName("sales.dimdate_gold") \
    .addColumn("OrderDate", DateType()) \
    .addColumn("Day", IntegerType()) \
    .addColumn("Month", IntegerType()) \
    .addColumn("Year", IntegerType()) \
    .addColumn("mmmyyyy", StringType()) \
    .addColumn("yyyymm", StringType()) \
    .execute()


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 5. Create dataframe dfdimDate_gold for dimDate_gold

# CELL ********************

from pyspark.sql.functions import col, dayofmonth, month, year, date_format
    
# Create dataframe for dimDate_gold
    
dfdimDate_gold = df.dropDuplicates(["OrderDate"]).select(col("OrderDate"), \
        dayofmonth("OrderDate").alias("Day"), \
        month("OrderDate").alias("Month"), \
        year("OrderDate").alias("Year"), \
        date_format(col("OrderDate"), "MMM-yyyy").alias("mmmyyyy"), \
        date_format(col("OrderDate"), "yyyyMM").alias("yyyymm"), \
    ).orderBy("OrderDate")

# Display the first 10 rows of the dataframe to preview your data

display(dfdimDate_gold.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 6. Load dfdimDate_gold to dimdate_gold table by Merge Parttern
# 
# Initial load (insert)

# CELL ********************

from delta.tables import *
    
deltaTable = DeltaTable.forPath(spark, 'Tables/dimdate_gold')
    
dfUpdates = dfdimDate_gold
    
deltaTable.alias('gold') \
  .merge(
    dfUpdates.alias('updates'),
    'gold.OrderDate = updates.OrderDate'
  ) \
   .whenMatchedUpdate(set =
    {
          
    }
  ) \
 .whenNotMatchedInsert(values =
    {
      "OrderDate": "updates.OrderDate",
      "Day": "updates.Day",
      "Month": "updates.Month",
      "Year": "updates.Year",
      "mmmyyyy": "updates.mmmyyyy",
      "yyyymm": "updates.yyyymm"
    }
  ) \
  .execute()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 7. Create structure for a dimcustomer_gold table

# CELL ********************

from pyspark.sql.types import *
from delta.tables import *
    
# Create customer_gold dimension delta table
DeltaTable.createIfNotExists(spark) \
    .tableName("sales.dimcustomer_gold") \
    .addColumn("CustomerName", StringType()) \
    .addColumn("Email",  StringType()) \
    .addColumn("First", StringType()) \
    .addColumn("Last", StringType()) \
    .addColumn("CustomerID", LongType()) \
    .execute()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 8. Transform dfdimCustomer_silver ()
# drop duplicate customers, select specific columns, and split the “CustomerName” column to create “First” and “Last” name columns:

# CELL ********************

from pyspark.sql.functions import col, split
    
# Create customer_silver dataframe
    
dfdimCustomer_silver = df.dropDuplicates(["CustomerName","Email"]).select(col("CustomerName"),col("Email")) \
    .withColumn("First",split(col("CustomerName"), " ").getItem(0)) \
    .withColumn("Last",split(col("CustomerName"), " ").getItem(1)) 
    
# Display the first 10 rows of the dataframe to preview your data

display(dfdimCustomer_silver.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# Here you have created a new DataFrame dfdimCustomer_silver by performing various transformations such as dropping duplicates, selecting specific columns, and splitting the “CustomerName” column to create “First” and “Last” name columns. The result is a DataFrame with cleaned and structured customer data, including separate “First” and “Last” name columns extracted from the “CustomerName” column.

# MARKDOWN ********************

# ##### 9. create the ID column (Incremental ID Start 0) for our customers
# generating unique CustomerID values using the monotonically_increasing_id() function.

# CELL ********************

from pyspark.sql.functions import monotonically_increasing_id, col, when, coalesce, max, lit
    
dfdimCustomer_temp = spark.read.table("Sales.dimCustomer_gold")
    
MAXCustomerID = dfdimCustomer_temp.select(coalesce(max(col("CustomerID")),lit(0)).alias("MAXCustomerID")).first()[0]
print("MAXCustomerID is ", MAXCustomerID)

# dfdimCustomer_silver left join dfdimCustomer_temp 
# ON silver.customername = customer_temp.customername and silver.email = temp_customer.email
dfdimCustomer_gold = dfdimCustomer_silver.join(dfdimCustomer_temp,(dfdimCustomer_silver.CustomerName == dfdimCustomer_temp.CustomerName) & (dfdimCustomer_silver.Email == dfdimCustomer_temp.Email), "left_anti")
    
# สร้างคอลัมน์ CustomerID เพื่อทำ auto_increment
dfdimCustomer_gold = dfdimCustomer_gold.withColumn("CustomerID",monotonically_increasing_id() + MAXCustomerID + 1)

# Display the first 10 rows of the dataframe to preview your data

display(dfdimCustomer_gold.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 10. Insert dfdimCustomer_gold to dimcustomer_gold table

# CELL ********************

from delta.tables import *

deltaTable = DeltaTable.forPath(spark, 'Tables/dimcustomer_gold')
    
dfUpdates = dfdimCustomer_gold
    
deltaTable.alias('gold') \
  .merge(
    dfUpdates.alias('updates'),
    'gold.CustomerName = updates.CustomerName AND gold.Email = updates.Email'
  ) \
   .whenMatchedUpdate(set =
    {
          
    }
  ) \
 .whenNotMatchedInsert(values =
    {
      "CustomerName": "updates.CustomerName",
      "Email": "updates.Email",
      "First": "updates.First",
      "Last": "updates.Last",
      "CustomerID": "updates.CustomerID"
    }
  ) \
  .execute()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 11. Create structure for a dimproduct_gold table

# CELL ********************

from pyspark.sql.types import *
from delta.tables import *
    
DeltaTable.createIfNotExists(spark) \
    .tableName("sales.dimproduct_gold") \
    .addColumn("ItemName", StringType()) \
    .addColumn("ItemID", LongType()) \
    .addColumn("ItemInfo", StringType()) \
    .execute()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 12. create the product_silver dataframe

# CELL ********************

# display silver dataframe
display(df.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.functions import col, split, lit, when
    
# Create product_silver dataframe
    
dfdimProduct_silver = df.dropDuplicates(["Item"]).select(col("Item")) \
    .withColumn("ItemName",split(col("Item"), ", ").getItem(0)) \
    .withColumn("ItemInfo",when((split(col("Item"), ", ").getItem(1).isNull() | (split(col("Item"), ", ").getItem(1)=="")),lit("")).otherwise(split(col("Item"), ", ").getItem(1))) 
    
# Display the first 10 rows of the dataframe to preview your data

display(dfdimProduct_silver.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 13. create IDs for your dimProduct_gold table
# 
# สร้าง auto increment ItemID ขึ้นมาใหม่

# CELL ********************

from pyspark.sql.functions import monotonically_increasing_id, col, lit, max, coalesce
    
#dfdimProduct_temp = dfdimProduct_silver
dfdimProduct_temp = spark.read.table("Sales.dimProduct_gold")
    
MAXProductID = dfdimProduct_temp.select(coalesce(max(col("ItemID")),lit(0)).alias("MAXItemID")).first()[0]
    
dfdimProduct_gold = dfdimProduct_silver.join(dfdimProduct_temp,(dfdimProduct_silver.ItemName == dfdimProduct_temp.ItemName) & (dfdimProduct_silver.ItemInfo == dfdimProduct_temp.ItemInfo), "left_anti")
    
dfdimProduct_gold = dfdimProduct_gold.withColumn("ItemID",monotonically_increasing_id() + MAXProductID + 1)
    
# Display the first 10 rows of the dataframe to preview your data

display(dfdimProduct_gold.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 14. Similar to what you’ve done with your other dimensions, you need to ensure that your product table remains up-to-date as new data comes in. In a new code block

# CELL ********************

from delta.tables import *
    
deltaTable = DeltaTable.forPath(spark, 'Tables/dimproduct_gold')
            
dfUpdates = dfdimProduct_gold
            
deltaTable.alias('gold') \
  .merge(
        dfUpdates.alias('updates'),
        'gold.ItemName = updates.ItemName AND gold.ItemInfo = updates.ItemInfo'
        ) \
        .whenMatchedUpdate(set =
        {
               
        }
        ) \
        .whenNotMatchedInsert(values =
         {
          "ItemName": "updates.ItemName",
          "ItemInfo": "updates.ItemInfo",
          "ItemID": "updates.ItemID"
          }
          ) \
          .execute()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 15. Create structure for the fact_sales_gold table

# CELL ********************

from pyspark.sql.types import *
from delta.tables import *
    
DeltaTable.createIfNotExists(spark) \
    .tableName("sales.factsales_gold") \
    .addColumn("CustomerID", LongType()) \
    .addColumn("ItemID", LongType()) \
    .addColumn("OrderDate", DateType()) \
    .addColumn("Quantity", IntegerType()) \
    .addColumn("UnitPrice", FloatType()) \
    .addColumn("Tax", FloatType()) \
    .execute()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 16. create a new dataframe to combine sales data with customer and product information include customer ID, item ID, order date, quantity, unit price, and tax

# CELL ********************

from pyspark.sql.functions import col
    
dfdimCustomer_temp = spark.read.table("Sales.dimCustomer_gold")
dfdimProduct_temp = spark.read.table("Sales.dimProduct_gold")
    
df = df.withColumn("ItemName",split(col("Item"), ", ").getItem(0)) \
    .withColumn("ItemInfo",when((split(col("Item"), ", ").getItem(1).isNull() | (split(col("Item"), ", ").getItem(1)=="")),lit("")).otherwise(split(col("Item"), ", ").getItem(1))) \

print("data frame df: ")
display(df.head(10))
    
# Create Sales_gold dataframe
    
dffactSales_gold = df.alias("df1").join(dfdimCustomer_temp.alias("df2"),(df.CustomerName == dfdimCustomer_temp.CustomerName) & (df.Email == dfdimCustomer_temp.Email), "left") \
        .join(dfdimProduct_temp.alias("df3"),(df.ItemName == dfdimProduct_temp.ItemName) & (df.ItemInfo == dfdimProduct_temp.ItemInfo), "left") \
    .select(col("df2.CustomerID") \
        , col("df3.ItemID") \
        , col("df1.OrderDate") \
        , col("df1.Quantity") \
        , col("df1.UnitPrice") \
        , col("df1.Tax") \
    ).orderBy(col("df1.OrderDate"), col("df2.CustomerID"), col("df3.ItemID"))
    
# Display the first 10 rows of the dataframe to preview your data
    
display(dffactSales_gold.head(10))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ##### 17. Insert data to factsales_gold table by merge operator

# CELL ********************

from delta.tables import *
    
deltaTable = DeltaTable.forPath(spark, 'Tables/factsales_gold')
    
dfUpdates = dffactSales_gold
    
deltaTable.alias('gold') \
  .merge(
    dfUpdates.alias('updates'),
    'gold.OrderDate = updates.OrderDate AND gold.CustomerID = updates.CustomerID AND gold.ItemID = updates.ItemID'
  ) \
   .whenMatchedUpdate(set =
    {
          
    }
  ) \
 .whenNotMatchedInsert(values =
    {
      "CustomerID": "updates.CustomerID",
      "ItemID": "updates.ItemID",
      "OrderDate": "updates.OrderDate",
      "Quantity": "updates.Quantity",
      "UnitPrice": "updates.UnitPrice",
      "Tax": "updates.Tax"
    }
  ) \
  .execute()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
