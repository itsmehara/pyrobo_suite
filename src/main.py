import argparse

# Importing your module files
from network_perf import exec_net_perf
from call_drop import exec_call_drop
from subscriber_seg import exec_sub_seg
from predict_maint import exec_pred_maint
from fraud_detection import exec_fraud_det
from billing_anomaly import exec_bill_anom
from network_optimize import exec_net_opt
from coverage_analysis import exec_cov_analy
from roam_pattern import exec_roam_pat
from cust_complaint import exec_cust_comp
from churn_predict import exec_churn_pred
from net_security import exec_net_sec
from qoe_analysis import exec_qoe_analy
from spectrum_optimize import exec_spec_opt
from comp_benchmark import exec_comp_bench

# Mapping module keywords to their respective execution functions
exec_map = {
    'net_perf': exec_net_perf,
    'call_drop': exec_call_drop,
    'sub_seg': exec_sub_seg,
    'pred_maint': exec_pred_maint,
    'fraud_det': exec_fraud_det,
    'bill_anom': exec_bill_anom,
    'net_opt': exec_net_opt,
    'cov_analy': exec_cov_analy,
    'roam_pat': exec_roam_pat,
    'cust_comp': exec_cust_comp,
    'churn_pred': exec_churn_pred,
    'net_sec': exec_net_sec,
    'qoe_analy': exec_qoe_analy,
    'spec_opt': exec_spec_opt,
    'comp_bench': exec_comp_bench,
}

def main():
    parser = argparse.ArgumentParser(description='PySpark Data Migration Project')
    parser.add_argument('--mod', type=str, help='Specify the module keyword to execute')
    args = parser.parse_args()

    # Check if the provided module keyword is valid
    if args.mod in exec_map:
        # Call the respective execution function for the specified module
        exec_map[args.mod]()
    else:
        print(f"Error: Invalid module keyword '{args.mod}'")

if __name__ == "__main__":
    main()
