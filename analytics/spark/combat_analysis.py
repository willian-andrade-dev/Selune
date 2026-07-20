from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BooleanType, TimestampType
from pyspark.sql import SparkSession

spark = (
    SparkSession
    .builder
    .appName('Combat_analysis')
    .getOrCreate()
)

schema = (
    StructType(  [
        StructField("id", IntegerType(), True),
        StructField("player_id", IntegerType(), True),
        StructField("monster_id", IntegerType(), True),
        StructField("monstro_nome", StringType(), True),
        StructField("xp_ganho", IntegerType(), True),
        StructField("gold_ganho", IntegerType(), True),
        StructField("vitoria", BooleanType(), True),
        StructField("duracao_ms", IntegerType(), True),
        StructField("data_hora", TimestampType(), True),
    ])
)

df = (
    spark
    .read
    .option("delimiter", ";")
    .option("header", "true")
    .schema(schema)
    .csv("analytics/spark/dados/combat_logs.csv")
)

df.printSchema()
df.show(5, truncate=False)

df.createOrReplaceTempView("combat_logs")

estatisticas = spark.sql("""
    SELECT
        monstro_nome,
        COUNT(*) AS total_combates,
        ROUND(SUM(CASE WHEN vitoria = true  THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as vitorias,
        ROUND(AVG(xp_ganho), 2) AS xp_medio,
        ROUND(AVG(gold_ganho), 2) AS gold_medio
    FROM combat_logs
    GROUP BY monstro_nome
""")

estatisticas.show(truncate=False)

estatisticas.coalesce(1).write.mode("overwrite").option("header", True).csv('analytics/spark/output/estatisticas_monstros')

spark.stop()