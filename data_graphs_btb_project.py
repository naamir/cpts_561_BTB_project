import btb_project
from btb_project import btb_main
from btb_project import print_stats
from btb_project import stats
from btb_project import wrong_addresses
from btb_project import print_wrong_addresses

abs_path_sample_trace = "C:\\Users\\nofal\\OneDrive\\Documents\\git\\cpts_561_BTB_project\\trace_sample.txt"
abs_path_Li_int = "C:\\Users\\nofal\\OneDrive\\Documents\\git\\cpts_561_BTB_project\\benchmark\\Li_int.txt"
abs_path_Spice_FP = "C:\\Users\\nofal\\OneDrive\\Documents\\git\\cpts_561_BTB_project\\benchmark\\Spice_FP.txt"

# manually change these flags as necessary
print_wrng_add_flag = True
print_Li_int_flag = False
print_Spice_FP_flag = True
# print("FILE:  Sample Trace\nlocal predictor\nInitial: STRONG TAKEN")
# # use STRONG TAKEN global even though not used
# # use Weak Non-Correlator eventhough not used in this case
# btb_main("local", abs_path_sample_trace) # use defaults
# print_stats(stats)
# print_wrong_addresses(wrong_addresses)

# print("\n\nFILE: Sample Trace\nglobal predictor\nInitial: STRONG TAKEN")
# btb_main("global", abs_path_sample_trace) # use defaults
# print_stats(stats)
# print_wrong_addresses(wrong_addresses)

# print("\n\nFILE: Sample Trace\nglobal predictor\nInitial: STRONG TAKEN")
# btb_main("tournament", abs_path_sample_trace) # use defaults
# print_stats(stats)
# print_wrong_addresses(wrong_addresses)

############## Li_int ###########################################
if print_Li_int_flag == True:
    print("FILE: Li_int\nlocal predictor\nInitial: STRONG TAKEN")
    btb_main("local", abs_path_Li_int) # use defaults
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)
    print("\n\nFILE: Li_int\nlocal predictor\nInitial: WEAK TAKEN")
    btb_main("local", abs_path_Li_int, init_local=[1,0])
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)

    print("\n\nFILE: Li_int\nglobal predictor\nInitial: STRONG TAKEN")
    btb_main("global", abs_path_Li_int) # use defaults
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)
    print("\n\nFILE: Li_int\nglobal predictor\nInitial: WEAK TAKEN")
    btb_main("global", abs_path_Li_int, init_global=[1,0])
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)

    print("\n\nFILE: Li_int\ntournament predictor\nInitial: STRONG TAKEN, Selector: Weak Non-Corelator(local)")
    btb_main("tournament", abs_path_Li_int) # use defaults
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)
    print("\n\nFILE: Li_int\ntournament predictor\nInitial: WEAK TAKEN, Selector: Weak Non-Corelator(local)")
    btb_main("tournament", abs_path_Li_int, init_local=[1,0], init_global=[1,0]) # use default selector
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)
    print("\n\nFILE: Li_int\ntournament predictor\nInitial: STRONG TAKEN, Selector: Weak Corelator(global)")
    btb_main("tournament", abs_path_Li_int, init_selector=[0,1]) # use default initial predictor states, i.e. STRONG TAKEN
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)
    print("\n\nFILE: Li_int\ntournament predictor\nInitial: WEAK TAKEN, Selector: Weak Corelator(global)")
    btb_main("tournament", abs_path_Li_int, init_local=[1,0], init_global=[1,0], init_selector=[0,1])
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)

############## Spice_FP ###########################################
if print_Spice_FP_flag == True:
    print("FILE: Spice_FP\nlocal predictor\nInitial: STRONG TAKEN")
    btb_main("local", abs_path_Spice_FP) # use defaults
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)
    print("\n\nFILE: Spice_FP\nlocal predictor\nInitial: WEAK TAKEN")
    btb_main("local", abs_path_Spice_FP, init_local=[1,0])
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)

    print("\n\nFILE: Spice_FP\nglobal predictor\nInitial: STRONG TAKEN")
    btb_main("global", abs_path_Spice_FP) # use defaults
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)
    print("\n\nFILE: Spice_FP\nglobal predictor\nInitial: WEAK TAKEN")
    btb_main("global", abs_path_Spice_FP, init_global=[1,0])
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)

    print("\n\nFILE: Spice_FP\ntournament predictor\nInitial: STRONG TAKEN, Selector: Weak Non-Corelator(local)")
    btb_main("tournament", abs_path_Spice_FP) # use defaults
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)
    print("\n\nFILE: Spice_FP\ntournament predictor\nInitial: WEAK TAKEN, Selector: Weak Non-Corelator(local)")
    btb_main("tournament", abs_path_Spice_FP, init_local=[1,0], init_global=[1,0]) # use default selector
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)
    print("\n\nFILE: Spice_FP\ntournament predictor\nInitial: STRONG TAKEN, Selector: Weak Corelator(global)")
    btb_main("tournament", abs_path_Spice_FP, init_selector=[0,1]) # use default initial predictor states, i.e. STRONG TAKEN
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)
    print("\n\nFILE: Spice_FP\ntournament predictor\nInitial: WEAK TAKEN, Selector: Weak Corelator(global)")
    btb_main("tournament", abs_path_Spice_FP, init_local=[1,0], init_global=[1,0], init_selector=[0,1])
    print_stats(stats)
    if print_wrng_add_flag == True:
        print_wrong_addresses(wrong_addresses)