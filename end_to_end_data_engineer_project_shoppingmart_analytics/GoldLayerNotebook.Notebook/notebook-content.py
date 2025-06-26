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

# ## GOLD LAYER NOTEBOOK: TRANSFORMANTIONS AND AGGREGATIONS SHOPPINGMART DATA

# CELL ********************

from pyspark.sql.functions import *

Orders_df = spark.read.table("shoppingmart_lakehouse.silver_customers_orderdata")
reviews_df = spark.read.table("shoppingmart_lakehouse.silver_review")
social_df = spark.read.table("shoppingmart_lakehouse.silver_social_media")
weblogs_df = spark.read.table("shoppingmart_lakehouse.silver_web_logs")
# display(social_df.head(100))



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### KPI1 : Aggregates web log data to measure engagement per user on each page and action.

# CELL ********************

weblogs_df = weblogs_df.groupBy("user_id", "page", "action").count()
# weblogs_df.write.mode("overwrite").parquet("Files/ShoppingMart_Gold_Web_Logs/ShoppingMart_web_logs")
weblogs_df.write.format("delta").mode("overwrite").saveAsTable("gold_web_logs")
display(weblogs_df.head(100))


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### KPI2 : Aggregates unstructured social media data to track sentiment trends across different platforms.

# CELL ********************

social_df= social_df.groupBy("platform","sentiment" ).count()
# # social_df.write.mode("overwrite").parquet("Files/ShoppingMart_Gold_Social_Media/ShoppingMart_social_media")
social_df.write.format("delta").mode("overwrite").saveAsTable("gold_social_media")
display(social_df.head(100))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# #### KPI3: Aggregates product reviews to calculate the average rating per product.

# CELL ********************

reviews_df = reviews_df.groupBy("product_id").agg(avg("rating").alias("AvgRating"))
# reviews_df.write.mode("overwrite").parquet("Files/ShoppingMart_Gold_Reviews/ShoppingMart_review")
reviews_df.write.format("delta").mode("overwrite").saveAsTable("gold_review")
display(reviews_df.head(100))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Orders_df.write.mode("overwrite").parquet("Files/ShoppingMart_Gold_Orders/ShoppingMart_customers_orderdata")
weblogs_df.write.format("delta").mode("overwrite").saveAsTable("gold_customers_orderdata")
display(Orders_df.head(100))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
