from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum

spark = SparkSession.builder.appName("StreamingVarejo").getOrCreate()

df_stream = spark.readStream.option("header", True).option("inferSchema", True).csv("../data/simulados")

vendas_categoria = df_stream.groupBy("categoria").agg(_sum("valor").alias("total_vendas"))

query = vendas_categoria.writeStream.outputMode("complete").format("console").start()

query.awaitTermination()
