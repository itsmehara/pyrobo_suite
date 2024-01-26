# pyrobo_suite

## PySpark Data Migration Project testing with robot framework.

A demo project integrating Robot Framework with Python. 

Learn to structure tests, handle dependencies, and generate insightful reports.



## Overview

This PySpark project is designed for data migration, involving the processing of various pipe-delimited text data files. The data is fetched from a specific folder, processed with necessary transformations and cleanup, and pushed to different tables based on the file name. Each file corresponds to a specific table, and the processing is done in parallel using PySpark.

## Project Structure

The project structure consists of two main directories:

### Python Project contain:

 
  * network_perf.py
  * call_drop.py
  * subscriber_seg.py
  * predict_maint.py
  * fraud_detection.py
  * billing_anomaly.py
  * network_optimize.py
  * coverage_analysis.py
  * roam_pattern.py
  * cust_complaint.py
  * churn_predict.py
  * net_security.py
  * qoe_analysis.py
  * spectrum_optimize.py
  * comp_benchmark.py
 
Each module will read pipe-delimited text file data from the source path using PySpark, perform basic transformations, and save the content to a SQLite database.
File names for the 15 modules:
1. `pyrobo_suite/src/`: Contains PySpark modules for different data processing tasks.
   - `network_perf.py`
   - `call_drop.py`
   - `subscriber_seg.py`
   - `predict_maint.py`
   - `fraud_detection.py`
   - `billing_anomaly.py`
   - `network_optimize.py`
   - `coverage_analysis.py`
   - `roam_pattern.py`
   - `cust_complaint.py`
   - `churn_predict.py`
   - `net_security.py`
   - `qoe_analysis.py`
   - `spectrum_optimize.py`
   - `comp_benchmark.py`
 
2. `pyrobo_suite/tests/`: Contains Robot Framework test cases for the PySpark modules.
   - `main_tests.robot`
   - `test_sample.robot`
   - `test_network_perf.robot`
   - `test_call_drop.robot`
   - `test_subscriber_seg.robot`
   - `test_predict_maint.robot`
   - `test_fraud_detection.robot`
   - `test_billing_anomaly.robot`
   - `test_network_optimize.robot`
   - `test_coverage_analysis.robot`
   - `test_roam_pattern.robot`
   - `test_cust_complaint.robot`
   - `test_churn_predict.robot`
   - `test_net_security.robot`
   - `test_qoe_analysis.robot`
   - `test_spectrum_optimize.robot`
   - `test_comp_benchmark.robot`

3. `pyrobo_suite/inbound/`: Contains inbound pipe-delimited data files for each module.
   - `network_performance_cols`: ["timestamp", "call_id", ...]
     - `network_performance_data_1011.txt`
     - `network_performance_data_1012.txt`
     - `network_performance_data_1013.txt`
     - `network_performance_data_1014.txt`
     - `network_performance_data_1015.txt`
     - `network_performance_data_1016.txt`
     - ...
   - `billing_anomalies_detection_cols`: ["timestamp", "subscriber_id", ...]
     - `billing_anomalies_data_1011.txt`
     - `billing_anomalies_data_1012.txt`
     - ...
   - `call_drop_analysis_cols`: ["timestamp", "call_id", ...]
     - `call_drop_data_1011.txt`
     - `call_drop_data_1012.txt`
     - ...
   - ...

## Modules and Columns

### Billing Anomalies Detection

Columns:
- timestamp
- subscriber_id
- call_charges
- data_usage_charges
- subscription_fees
- billing_anomaly_indicator
- location
- device_model
- operator
- anomaly_type
- anomaly_severity
- billing_result

### Call Drop Analysis

Columns:
- timestamp
- call_id
- caller_number
- receiver_number
- call_duration
- call_type
- call_drop_status
- location
- device_model
- operator
- call_reason
- call_result

### Churn Prediction

Columns:
- subscriber_id
- timestamp
- call_drops
- network_issues
- customer_satisfaction_score
- churn_indicator
- location
- device_model
- operator
- data_usage
- call_quality
- network_type
- contract_duration
- monthly_bill
- churn_reason
- churn_result

### Process Network Performance

Columns:
- timestamp
- device_id
- location
- latency
- throughput
- packet_loss
- connection_type
- network_type
- signal_strength
- data_usage
- call_quality
- device_model
- operator
- roaming_status

## Running the Project

* To run the project, execute the `main.py` script with the desired command line parameters. For example:
* To main.py following keywords will be passed respectively.
   - network_perf.py - net_perf 
   - call_drop.py - call_drop 
   - subscriber_seg.py - sub_seg 
   - predict_maint.py - pred_maint 
   - fraud_detection.py - fraud_det 
   - billing_anomaly.py - bill_anom 
   - network_optimize.py - net_opt 
   - coverage_analysis.py - cov_analy 
   - roam_pattern.py - roam_pat 
   - cust_complaint.py - cust_comp 
   - churn_predict.py - churn_pred 
   - net_security.py - net_sec 
   - qoe_analysis.py - qoe_analy 
   - spectrum_optimize.py - spec_opt 
   - comp_benchmark.py - comp_bench 

# Running PySpark Modules

### Example Commands

#### Network Performance (net_perf)
```bash
python main.py --mod net_perf
```


#### Call Drop Analysis (call_drop)
```bash
python main.py --mod call_drop
```

#### Subscriber Segmentation (sub_seg)
```bash
python main.py --mod sub_seg
```

#### Predictive Maintenance (pred_maint)
```bash
python main.py --mod pred_maint
```

#### Fraud Detection (fraud_det)
```bash
python main.py --mod fraud_det
```

#### Billing Anomalies Detection (bill_anom)
```bash
python main.py --mod bill_anom
```

#### Network Optimization (net_opt)
```bash
python main.py --mod net_opt
```

#### Coverage Analysis (cov_analy)
```bash
python main.py --mod cov_analy
```

#### Roaming Pattern Analysis (roam_pat)
```bash
python main.py --mod roam_pat
```

#### Customer Complaint Analysis (cust_comp)
```bash
python main.py --mod cust_comp
```

#### Churn Prediction (churn_pred)
```bash
python main.py --mod churn_pred
```

#### Network Security Analysis (net_sec)
```bash
python main.py --mod net_sec
```

#### Quality of Experience Analysis (qoe_analy)
```bash
python main.py --mod qoe_analy
```

#### Spectrum Utilization Optimization (spec_opt)
```bash
python main.py --mod spec_opt
```

#### Competitive Benchmarking (comp_bench)
```bash
python main.py --mod comp_bench
```

