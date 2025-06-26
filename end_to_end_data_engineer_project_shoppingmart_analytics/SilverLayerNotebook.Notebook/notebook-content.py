# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "b8f991a4-df6e-425b-80a2-43a82263fd55",
# META       "default_lakehouse_name": "shoppingmart_lakehouse",
# META       "default_lakehouse_workspace_id": "9caebd0d-2a58-418d-a2af-7b6a694302c9",
# META       "known_lakehouses": [
# META         {
# META           "id": "b8f991a4-df6e-425b-80a2-43a82263fd55"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# ## SILVER LAYER NOTEBOOK: DATA CLEANING AND INTEGRATION

# MARKDOWN ********************

# #### LOAD DATA FROM BRONZE LAYER

# CELL ********************

from pyspark.sql.functions import *

df_customers = spark.read.format("csv").option("header","true").load("Files/ShoppingMart_Bronze_Customers/ShoppingMart_customers.csv")
df_orders = spark.read.format("csv").option("header","true").load("Files/ShoppingMart_Bronze_Orders/ShoppingMart_orders.csv")
df_products = spark.read.format("csv").option("header","true").load("Files/ShoppingMart_Bronze_Products/ShoppingMart_products.csv")
df_reviews = spark.read.json("Files/ShoppingMart_Bronze_Reviews/ShoppingMart_review.json")
df_social = spark.read.json("Files/ShoppingMart_Bronze_Social_Media/ShoppingMart_social_media.json")
df_weblogs = spark.read.json("Files/ShoppingMart_Bronze_Web_Logs/ShoppingMart_web_logs.json")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### DATA CLEANING AND ENRICHING

# CELL ********************

df_orders = df_orders.dropna(subset = ["OrderID", "CustomerID", "ProductID", "OrderDate", "TotalAmount"])
df_orders = df_orders.withColumn("OrderDate", to_date(col("OrderDate")))
# display(df_orders)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### JOIN WITH PRODUCTS & CUSTOMERS

# CELL ********************

df_orders = df_orders \
    .join (df_customers, on = 'CustomerID', how = "inner") \
    .join (df_products, on = 'ProductID', how = "inner")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print("df_orders", df_orders.count())
print("df_reviews", df_reviews.count())
print("df_social", df_social.count())
print("df_weblogs", df_weblogs.count())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### WRITE DATA TO SILVER LAYER

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# df_orders.write.mode("overwrite").parquet("Files/ShoppingMart_Silver_Orders/ShoppingMart_customers_orderdata")
# df_reviews.write.mode("overwrite").parquet("Files/ShoppingMart_Silver_Reviews/ShoppingMart_review")
# df_social.write.mode("overwrite").parquet("Files/ShoppingMart_Silver_Social_Media/ShoppingMart_social_media")
# df_weblogs.write.mode("overwrite").parquet("Files/ShoppingMart_Silver_Web_Logs/ShoppingMart_web_logs")

df_orders.write.format("delta").mode("overwrite").saveAsTable("silver_customers_orderdata")
df_reviews.write.format("delta").mode("overwrite").saveAsTable("silver_review")
df_social.write.format("delta").mode("overwrite").saveAsTable("silver_social_media")
df_weblogs.write.format("delta").mode("overwrite").saveAsTable("silver_web_logs")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
