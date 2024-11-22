# Databricks notebook source
# MAGIC %md
# MAGIC <font size="5" color="red">Task1 : Sunday Sales Analysis for Silver Products</font>

# COMMAND ----------

from pyspark.sql.functions import col, sum, avg
from pyspark.sql.types import FloatType

spark = SparkSession.builder \
    .appName("Homework 11") \
    .getOrCreate()

internet = spark.read.csv('/FileStore/tables/fact_internet_sales.csv', header=True, inferSchema=True)
currency = spark.read.csv('/FileStore/tables/dim_currency.csv', header=True, inferSchema=True)
customer = spark.read.csv('/FileStore/tables/dim_customer.csv', header=True, inferSchema=True)
product = spark.read.csv('/FileStore/tables/dim_product.csv', header=True, inferSchema=True)
date = spark.read.csv('/FileStore/tables/dim_date.csv', header=True, inferSchema=True)

# currency-CurrencyKey
# internet-CurrencyKey, ProductKey, OrderDateKey, CustomerKey, CurrencyKey
# customer-CustomerKey
# product-ProductKey
# date-OrderDateKey
internet = internet.withColumnRenamed("OrderDateKey", "DateKey")

internet_with_currency = internet.join(currency, on="CurrencyKey", how="inner")
internet_with_customer = internet_with_currency.join(customer, on="CustomerKey", how="inner")
internet_with_product = internet_with_customer.join(product, on="ProductKey", how="inner")
df = internet_with_product.join(date, on="DateKey", how="inner")

# Consider sales that occurred on Sundays.
df_sunday = df.filter(col("EnglishDayNameOfWeek")=='Sunday')

# Include only products where:
# Color is Silver.
# Has Size information.
# Weight is greater than 10.
only_products = df_sunday.filter((col("Color") == "Silver") &(col("Size").isNotNull()) &(col("Weight") > 10))

# Include customers who:
# Have a YearlyIncome greater than 100,000.0.
# Have more than 1 child.
customers_filter = only_products.filter((col("YearlyIncome")>100000) & (col("TotalChildren")>1))

# 2. Aggregations:
# Group by CustomerKey and FirstName.
# Calculate the following metrics:
# Total TaxAmt paid by each customer.
# Average SalesAmount.
# Average TotalProductCost.
customers_filter = customers_filter.withColumn("TaxAmt", col("TaxAmt").cast(FloatType())) \
                           .withColumn("SalesAmount", col("SalesAmount").cast(FloatType())) \
                           .withColumn("TotalProductCost", col("TotalProductCost").cast(FloatType()))

groupingBY = customers_filter.groupBy("CustomerKey", "FirstName").agg(sum('TaxAmt').alias('TotalAmt'), avg('SalesAmount').alias('AvgSalesAmt'), avg('TotalProductCost').alias('AvgProductCost'))

# 3. Sorting:
# Sort the result by FirstName in ascending order.
orderingBY = groupingBY.orderBy("FirstName", ascending=True)

# 4. Data Presentation:
# Drop the CustomerKey column from the final output.
presentation = orderingBY.drop('CustomerKey')
presentation.show()
