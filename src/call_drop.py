# call_drop_analysis.
# (Similar structure as above with column names and transformations for call_drop_analysis module)
import constants as c
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit
from pyspark.sql.functions import input_file_name, regexp_extract
mod_name = "call_drop_analysis"


def call_drop_analysis():
    call_drop_analysis_cols = ["timestamp", "call_id", "caller_number", "receiver_number", "call_duration", "call_type",
               "call_drop_status", "location", "device_model", "operator", "call_reason", "call_result"]


def exec_call_drop(module):
    # Initialize Spark session
    # spark = SparkSession.builder.appName("NetworkPerformance").getOrCreate()
    spark = SparkSession.builder \
                        .appName(c.app_name) \
                        .config("spark.jars", "../driver_sqlite/sqlite-jdbc-3.45.0.0.jar") \
                        .getOrCreate()

    # # Define the module specific columns
    # net_perf_cols = ["timestamp", "device_id", "location", "latency", "throughput", "packet_loss",
    #                  "connection_type", "network_type", "signal_strength", "data_usage", "call_quality",
    #                  "device_model", "operator", "roaming_status"]

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
    exec_call_drop(c.call_drop)
