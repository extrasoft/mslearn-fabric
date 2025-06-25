# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "0b9a43aa-e391-462b-83c9-8db3f5f290ba",
# META       "default_lakehouse_name": "lab18_lakehouse",
# META       "default_lakehouse_workspace_id": "3fd6a85a-8c02-4d5a-9f0e-27028a843272",
# META       "known_lakehouses": [
# META         {
# META           "id": "0b9a43aa-e391-462b-83c9-8db3f5f290ba"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM lab18_lakehouse.products LIMIT 1000")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
