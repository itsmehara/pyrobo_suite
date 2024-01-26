# network_performance.
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col
from pyspark.sql.functions import lit


def process_network_performance(spark):
    # Define column list
    process_network_performance_cols = ["timestamp", "device_id", "location", "latency", "throughput", "packet_loss", "connection_type",
               "network_type", "signal_strength", "data_usage", "call_quality", "device_model", "operator",
               "roaming_status"]
    columns = ["timestamp", "device_id", "location", "latency", "throughput", "packet_loss", "connection_type", "network_type", "signal_strength", "data_usage", "call_quality", "device_model", "operator", "roaming_status"]

    # Read data
    data = spark.read.text("path_to_data/network_performance_data.txt")

    # Split pipe-delimited data into columns
    split_data = data.select(split(col("value"), "\|").alias("data"))

    # Define transformations
    processed_data = split_data.selectExpr(*[f"data[{i}] as {columns[i]}" for i in range(len(columns))])

    # Save to SQLite
    processed_data.write.mode("overwrite").option("header", "true").jdbc("jdbc:sqlite:path_to_db/network_performance.db", "network_performance", properties={"driver": "org.sqlite.JDBC"})


def exec_net_perf_old():
    spark_session = SparkSession.builder.appName("NetworkPerformance").getOrCreate()
    process_network_performance(spark_session)
    spark_session.stop()


def exec_net_perf():
    # Initialize Spark session
    spark = SparkSession.builder.appName("NetworkPerformance").getOrCreate()

    # Define the path to the inbound folder
    inbound_folder_path = "./pyrobo_suite/inbound/"

    # Define the module specific columns
    net_perf_cols = ["timestamp", "device_id", "location", "latency", "throughput", "packet_loss",
                     "connection_type", "network_type", "signal_strength", "data_usage", "call_quality",
                     "device_model", "operator", "roaming_status"]

    # Define the target SQLite database and table
    sqlite_db_path = "net_perf_db.db"
    table_name = "net_perf_table"

    # Create an empty DataFrame to hold the combined data
    combined_df = spark.createDataFrame([], schema=net_perf_cols)

    # Loop through each file in the inbound folder
    for file_code in ["1011", "1012", "1013", "1014", "1015", "1016"]:
        file_path = f"{inbound_folder_path}network_performance_data_{file_code}.txt"

        # Read the file into a DataFrame, skip header, and add file_code column
        file_df = spark.read.option("header", "true").option("delimiter", "|").csv(file_path)
        file_df = file_df.withColumn("file_code", lit(file_code))

        # Append the DataFrame to the combined DataFrame
        combined_df = combined_df.union(file_df)

    # Save the combined DataFrame to the SQLite database
    combined_df.write.format("jdbc").option("url", f"jdbc:sqlite:{sqlite_db_path}").option("dbtable", table_name).mode("append").save()

    # Stop the Spark session
    spark.stop()


if __name__ == "__main__":
    # Execute the network performance module
    exec_net_perf()
