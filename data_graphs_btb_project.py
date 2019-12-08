import btb_project
from btb_project import btb_main
from btb_project import print_stats
from btb_project import stats
from btb_project import wrong_addresses
from btb_project import print_wrong_addresses

abs_path_sample_trace = "C:\\Users\\nofal\\OneDrive\\Documents\\git\\cpts_561_BTB_project\\trace_sample.txt"
abs_path_Li_int = "C:\\Users\\nofal\\OneDrive\\Documents\\git\\cpts_561_BTB_project\\benchmark\\Li_int.txt"
abs_path_Spice_FP = "C:\\Users\\nofal\\OneDrive\\Documents\\git\\cpts_561_BTB_project\\benchmark\\Spice_FP.txt"

print("DATA: local predictor")
btb_main("local", abs_path_sample_trace)
print_stats(stats)
print_wrong_addresses(wrong_addresses)

print("DATA: global predictor")
btb_main("global", abs_path_sample_trace)
print_stats(stats)
print_wrong_addresses(wrong_addresses)

print("DATA: tournament predictor")
btb_main("tournament", abs_path_sample_trace)
print_stats(stats)
print_wrong_addresses(wrong_addresses)