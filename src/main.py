import argparse
import constants as c
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
    c.net_perf: exec_net_perf,
    c.call_drop: exec_call_drop,
    c.sub_seg: exec_sub_seg,
    c.pred_maint: exec_pred_maint,
    c.fraud_det: exec_fraud_det,
    c.bill_anom: exec_bill_anom,
    c.net_opt: exec_net_opt,
    c.cov_analy: exec_cov_analy,
    c.roam_pat: exec_roam_pat,
    c.cust_comp: exec_cust_comp,
    c.churn_pred: exec_churn_pred,
    c.net_sec: exec_net_sec,
    c.qoe_analy: exec_qoe_analy,
    c.spec_opt: exec_spec_opt,
    c.comp_bench: exec_comp_bench
}


def main():
    parser = argparse.ArgumentParser(description='PySpark Data Migration Project')
    parser.add_argument('--mod', type=str, help='Specify the module keyword to execute')
    args = parser.parse_args()

    # Check if the provided module keyword is valid
    if args.mod in exec_map:
        # Call the respective execution function for the specified module
        mod_name = args.mod[:]
        exec_map[args.mod](mod_name)
    else:
        print(f"Error: Invalid module keyword '{args.mod}'")


if __name__ == "__main__":
    main()
