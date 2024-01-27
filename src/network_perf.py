# network_performance.
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col
from pyspark.sql.functions import lit
from pyspark.sql.functions import input_file_name, regexp_extract
import os
mod_name = "network_performance_data"

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


def exec_net_perf_old1():
    spark_session = SparkSession.builder.appName("NetworkPerformance").getOrCreate()
    process_network_performance(spark_session)
    spark_session.stop()


def exec_net_perf_old2():
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


def exec_net_perf_old3():
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

    # Read all files matching the pattern into a DataFrame
    file_path = f"{inbound_folder_path}network_performance_data_*.txt"
    combined_df = spark.read.option("header", "true").option("delimiter", "|").csv(file_path)

    # Extract the file_code from the file name using regexp_extract
    combined_df = combined_df.withColumn("file_code", regexp_extract(input_file_name(), r'data_(\d+).txt', 1))

    # Save the DataFrame to the SQLite database
    combined_df.write.format("jdbc").option("url", f"jdbc:sqlite:{sqlite_db_path}").option("dbtable", table_name).mode("append").save()

    # Stop the Spark session
    spark.stop()


def extract_file_info(file_path):
    # Extract area_code, zone_code, module_name, date, and file_code from the file path
    pattern = r'(\w{2})_(\w{2})_(\w+)_network_performance_data_(\d{8})_(\d{4}).txt'
    matches = re.search(pattern, file_path)

    if matches:
        area_code, zone_code, module_name, date, file_code = matches.groups()
        return area_code, zone_code, module_name, date, file_code
    else:
        return None


def exec_net_perf():
    # Initialize Spark session
    # spark = SparkSession.builder.appName("NetworkPerformance").getOrCreate()
    spark = SparkSession.builder \
                        .appName("YourAppName") \
                        .config("spark.jars", "/path/to/sqlite-jdbc-<version>.jar") \
                        .getOrCreate()

    # Define the path to the inbound folder
    inbound_folder_path = "../inbound/"

    # Define the module specific columns
    net_perf_cols = ["timestamp", "device_id", "location", "latency", "throughput", "packet_loss",
                     "connection_type", "network_type", "signal_strength", "data_usage", "call_quality",
                     "device_model", "operator", "roaming_status"]

    # Define the target SQLite database and table
    sqlite_db_path = "net_perf_db.db"
    table_name = "net_perf_table"

    # Read all files matching the pattern into a DataFrame
    file_path = f"{inbound_folder_path}{mod_name}_*.txt"
    combined_df = spark.read.option("header", "true").option("delimiter", "|").csv(file_path)
    # Extract the current process ID
    process_id = spark.sparkContext.applicationId
    reg_exp = r'(\w{2})_(\w{2})_(\w+)_network_performance_data_(\d{8})_(\d{4}).txt'
    # Extract additional information from the file path
    combined_df = (combined_df.withColumn("area_code", regexp_extract(input_file_name(), reg_exp, 1))
                              .withColumn("zone_code", regexp_extract(input_file_name(), reg_exp, 2))
                              .withColumn("module_name", regexp_extract(input_file_name(), reg_exp, 3))
                              .withColumn("date", regexp_extract(input_file_name(), reg_exp, 4))
                              .withColumn("file_code", regexp_extract(input_file_name(), reg_exp, 5))
                              .withColumn("process_id", lit(process_id) ))

    # Save the DataFrame to the SQLite database
    (combined_df.write.format("jdbc")
                      .option("url", f"jdbc:sqlite:{sqlite_db_path}")
                      .option("dbtable", table_name)
                      .option("driver", "org.sqlite.JDBC")  # Specify the JDBC driver class name
                      .mode("overwrite")
                      .save())

    # Stop the Spark session
    spark.stop()


if __name__ == "__main__":
    # Execute the network performance module
    exec_net_perf()
