import btb_project
from btb_project import btb_main
from btb_project import print_BTB
from btb_project import stats

abs_path_sample_trace = "C:\\Users\\nofal\\OneDrive\\Documents\\git\\cpts_561_BTB_project\\trace_sample.txt"
abs_path_Li_int = "C:\\Users\\nofal\\OneDrive\\Documents\\git\\cpts_561_BTB_project\\benchmark\\Li_int.txt"
abs_path_Spice_FP = "C:\\Users\\nofal\\OneDrive\\Documents\\git\\cpts_561_BTB_project\\benchmark\\Spice_FP.txt"

btb_main("local", abs_path_sample_trace)
print_BTB(stats)