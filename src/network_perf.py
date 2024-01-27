# network_performance.
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col
from pyspark.sql.functions import lit
from pyspark.sql.functions import input_file_name, regexp_extract
import constants as c
mod_name = "network_performance_data"


def extract_file_info(file_path):
    # Extract area_code, zone_code, module_name, date, and file_code from the file path
    pattern = r'(\w{2})_(\w{2})_(\w+)_network_performance_data_(\d{8})_(\d{4}).txt'
    matches = re.search(pattern, file_path)

    if matches:
        area_code, zone_code, module_name, date, file_code = matches.groups()
        return area_code, zone_code, module_name, date, file_code
    else:
        return None


def exec_net_perf(module):
    # Initialize Spark session
    # spark = SparkSession.builder.appName("NetworkPerformance").getOrCreate()
    spark = SparkSession.builder \
                        .appName(c.app_name) \
                        .config("spark.jars", "../driver_sqlite/sqlite-jdbc-3.45.0.0.jar") \
                        .getOrCreate()

    # Define the module specific columns
    net_perf_cols = ["timestamp", "device_id", "location", "latency", "throughput", "packet_loss",
                     "connection_type", "network_type", "signal_strength", "data_usage", "call_quality",
                     "device_model", "operator", "roaming_status"]

    # Define the target SQLite database and table
    sqlite_db_path = c.sqlite_db_path
    table_name = f"{module}_table"
    outbound_csv = f"{c.outbound_folder_path}/{module}"

    # Read all files matching the pattern into a DataFrame
    file_path = f"{c.inbound_folder_path}{mod_name}_*.txt"
    combined_df = spark.read.option("header", "true").option("delimiter", "|").csv(file_path)
    # Extract the current process ID
    process_id = spark.sparkContext.applicationId
    reg_exp = r'(\w)_(\d{8})_(\d{4}).txt'
    # Extract additional information from the file path
    combined_df = (combined_df.withColumn("module_name", lit(module))
                              .withColumn("date", regexp_extract(input_file_name(), reg_exp, 2))
                              .withColumn("file_code", regexp_extract(input_file_name(), reg_exp, 3))
                              .withColumn("process_id", lit(process_id) ))

    combined_df.write.csv(outbound_csv, header=True, mode="overwrite")

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
    exec_net_perf(c.net_perf)
