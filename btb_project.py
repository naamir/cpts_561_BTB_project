import sys
import logging
import argparse

####### I N I T #####################
btb = dict()
# for predictor state machine
TAKEN = 1
NOT_TAKEN = 0
# for selector state machine
CORRECT = 1
WRONG = 0

wrong_addresses = dict()

stats = {
    "hits": 0,
    "misses":	0,
	"correct_pred": 0,
	"wrong_pred": 0,
	"collisions": 0
}
m_type = 0
m_codefile = 0
global_hist = [0,0]

# logging only for ERROR to make it faster
logging.basicConfig(filename='cpts561_log.log', filemode='w', level=logging.ERROR)

####### F U N C T I O N S #####################
def flush_data():
    btb.clear()
    wrong_addresses.clear()
    stats["hits"] = 0
    stats["misses"] = 0
    stats["correct_pred"] = 0
    stats["collisions"] = 0


def get_entry_BTB(code):
    ''' assume input as hex'''
    # the BTB will be a dictionary with index determined from last 3 words of PC
    # i.e. 400>1c4< -> 1*16^2 + 12+16 + 4 = 452 >> 2 (right-shift by 2 OR divide by 4)
    #     ..>0001 1100 01<00
    total = 0
    last_three = code[3:6]
    # reverse them so math is easier
    last_three = "".join(reversed(last_three))
    for i in range(0, len(last_three)):
        total = total + int(last_three[i], 16) * (16**i)
        logging.debug("i {} -hex {} -dec {} -total {}".format(i, 
                                                        last_three[i], 
                                                        int(last_three[i], 16), total))
    
    # divide by 4
    entry = total >> 2
    logging.info("entry number for BTB: {}".format(entry))
    return entry

def update_BTB(entry, **kwargs):
    ''' this is where data is added to BTB '''
    # mod so we only have 1024 entries
    # btb--> {entry : {pc, tpc, local_pred, g00, g01, g10, g11, sel} ....}
    if in_BTB(entry, verbose=False) == True:
        for key, val in kwargs.items():
            if key == "pc":
                # we are updating the BTB hence we should check if there is a collision
                check_collision(entry, val)
            btb[entry][key] = val
    else:
        # create new entry in BTB
        temp_btb = dict()
        for key, val in kwargs.items():
            # print("key:{}, val:{}".format(key, val))
            temp_btb[key] = val

        btb[entry % 1024] = temp_btb

def print_wrong_addresses(wrong_addrs):
    print("actual target pc     wrong BTB target pc")
    for key, val in wrong_addrs.items():
        print(key, "            ", val)
    
def print_stats(stats):
    print("\nhits:{} -- misses:{} -- right predictions:{} -- wrong predictions:{} -- collisions:{}".format(
                                                    stats["hits"],
                                                    stats["misses"],
                                                    stats["correct_pred"],
                                                    stats["wrong_pred"],
                                                    stats["collisions"]))
    hit_rate = stats["hits"] / (stats["hits"] + stats["misses"]) * 100
    pred_accuracy = stats["correct_pred"] / stats["hits"] * 100
    print("hit rate:{} -- prediction accuracy:{}".format(hit_rate, pred_accuracy))
        
def print_BTB(ptype, sort=False):
    if sort == True:
        if ptype == "local":
            sorted_btb = sorted(btb)
            for entry in sorted_btb:
                print("{} --- PC {} - targetPC {} - local_pred {}".format(entry,
                                                            btb[entry]["pc"], 
                                                            btb[entry]["tpc"],
                                                            btb[entry]["local_pred"]))
        elif ptype == "global":
            sorted_btb = sorted(btb)
            for entry in sorted_btb:
                print("{} --- PC {} - targetPC {} - g00 {} - g01 {} - g01 {} - g11 {}".format(entry,
                                                            btb[entry]["pc"], 
                                                            btb[entry]["tpc"],
                                                            btb[entry]["g00"],
                                                            btb[entry]["g01"],
                                                            btb[entry]["g10"],
                                                            btb[entry]["g11"]))
        elif ptype == "tournament":
            sorted_btb = sorted(btb)
            for entry in sorted_btb:
                print("{} --- PC {} - targetPC {} - g00 {} - g01 {} - g01 {} - g11 {} - local {} - sel {}".format(entry,
                                                            btb[entry]["pc"], 
                                                            btb[entry]["tpc"],
                                                            btb[entry]["g00"],
                                                            btb[entry]["g01"],
                                                            btb[entry]["g10"],
                                                            btb[entry]["g11"],
                                                            btb[entry]["local_pred"],
                                                            btb[entry]["sel"]))
    elif sort == False:
        if ptype == "local":
            for entry in btb:
                print("{} --- PC {} - targetPC {} - local_pred {}".format(entry, 
                                                            btb[entry]["pc"], 
                                                            btb[entry]["tpc"],
                                                            btb[entry]["local_pred"]))
        
        elif ptype == "global":
            for entry in btb:
                print("{} --- PC {} - targetPC {} - g00 {} - g01 {} - g01 {} - g11 {}".format(entry,
                                                            btb[entry]["pc"], 
                                                            btb[entry]["tpc"],
                                                            btb[entry]["g00"],
                                                            btb[entry]["g01"],
                                                            btb[entry]["g10"],
                                                            btb[entry]["g11"]))
        elif ptype == "tournament":
            for entry in btb:
                print("{} --- PC {} - targetPC {} - g00 {} - g01 {} - g01 {} - g11 {} - local {} - sel {}".format(entry,
                                                            btb[entry]["pc"], 
                                                            btb[entry]["tpc"],
                                                            btb[entry]["g00"],
                                                            btb[entry]["g01"],
                                                            btb[entry]["g10"],
                                                            btb[entry]["g11"],
                                                            btb[entry]["local_pred"],
                                                            btb[entry]["sel"]))
def in_BTB(entry, pc=None, verbose=True):
    if verbose == True:
        if entry in btb:
            logging.debug("entry in BTB!")
            if pc == btb[entry]["pc"]:
                logging.debug("PC found in BTB!")
                if m_type == "local":
                    logging.debug("BTB entry {} --- PC {} - targetPC {} - local_pred {}".
                                                            format(entry, 
                                                            btb[entry]["pc"], 
                                                            btb[entry]["tpc"],
                                                            btb[entry]["local_pred"]))
                elif m_type == "global":
                    logging.debug("{} --- PC {} - targetPC {} - g00 {} - g01 {} - g01 {} - g11 {}".format(entry,
                                                            btb[entry]["pc"], 
                                                            btb[entry]["tpc"],
                                                            btb[entry]["g00"],
                                                            btb[entry]["g01"],
                                                            btb[entry]["g10"],
                                                            btb[entry]["g11"]))
                return True
        else:
            logging.debug("PC {} not in BTB".format(pc))
            return False
    else:
        if entry in btb:
            return True
        else:
            return False

def update_global_hist(t_nt):
    # whatever index 0 had in not relevant anymore
    # replace with previous state
    global_hist[0] = global_hist[1]
    global_hist[1] = t_nt

    logging.debug("global history: {}".format(global_hist))

def update_pred(prev_pred, t_nt):
    # implement 2-bit prdictor state-machine
    # input1: previous prediction (in [x,x] format)
    # input2: current branch TAKEN(=1) or NOT_TAKEN(=0)

    # if previous Strong Taken and actual branch TAKEN
    if (((prev_pred[0] == TAKEN) and (prev_pred[1] == TAKEN))
         and (t_nt == TAKEN)):
        # stay in Strong Taken
        new_pred = [1,1]
    # if previous Strong Taken and actual branch NOT_TAKEN
    elif (((prev_pred[0] == TAKEN) and (prev_pred[1] == TAKEN))
         and (t_nt == NOT_TAKEN)):
        # transition to Weak Taken
        new_pred = [1,0]
    # if previous Weak Taken and actual branch TAKEN
    elif (((prev_pred[0] == TAKEN) and (prev_pred[1] == NOT_TAKEN))
         and (t_nt == TAKEN)):
        # transition to Strong Taken
        new_pred = [1,1]
    # if previous Weak Taken and actual branch NOT_TAKEN
    elif (((prev_pred[0] == TAKEN) and (prev_pred[1] == NOT_TAKEN))
         and (t_nt == NOT_TAKEN)):
        # transition to Strong Not Taken
        new_pred = [0,0]
    # if previous Strong Not Taken and actual branch NOT_TAKEN
    elif (((prev_pred[0] == NOT_TAKEN) and (prev_pred[1] == NOT_TAKEN))
         and (t_nt == NOT_TAKEN)):
        # stay in Strong Not Taken
        new_pred = [0,0]
    # if previous Strong Not Taken and actual branch TAKEN
    elif (((prev_pred[0] == NOT_TAKEN) and (prev_pred[1] == NOT_TAKEN))
         and (t_nt == TAKEN)):
        # transition to Weak Not Taken
        new_pred = [0,1]
    # if previous Weak Not Taken and actual branch TAKEN
    elif (((prev_pred[0] == NOT_TAKEN) and (prev_pred[1] == TAKEN))
         and (t_nt == TAKEN)):
        # transition to Strong Taken
        new_pred = [1,1]
    # if previous Weak Not Taken and actual branch NOT_TAKEN
    elif (((prev_pred[0] == NOT_TAKEN) and (prev_pred[1] == TAKEN))
         and (t_nt == NOT_TAKEN)):
        # transition to Strong Not Taken
        new_pred = [0,0]
    
    return new_pred

def update_selector(prev_sel, mlocal, mglobal):
    # implement 2-bit selector state machine
    # input1(prev_sel): previously used selector i.e. either correlator (global predictor) or non-correlator (local predictor)
    # input2(mlocal): whether non-correlator (local) was CORRECT(=1) or WRONG(=0)
    # input3(mglobal): whether correlator (global) was CORRECT(=1) or WRONG(=0)

    # if previous Strong Correlator
    # all conditions to stay in Strong Correlator
    if (((prev_sel == [0,0]) and
        ((mlocal == WRONG and mglobal == WRONG) or # if both are WRONG (0/0)
        (mlocal == WRONG and mglobal == CORRECT)) or # if local is WRONG and global is CORRECT (0/1)
        (mlocal == CORRECT and mglobal == CORRECT))):  # if both are CORRECT (1/1)
        
        new_sel = [0,0]
    # if previous Strong Correlator
    # condition to move to Weak Correlator
    elif ((prev_sel == [0,0]) and (mlocal == CORRECT and  mglobal == WRONG)):
        new_sel = [0,1]

    # if previous Weak Correlator
    # all conditions to stay in Weak Correlator
    elif ((prev_sel == [0,1] and
        ((mlocal == WRONG and mglobal == WRONG) or # if both are WRONG (0/0)
        (mlocal == CORRECT and mglobal == CORRECT)))):  # if both are CORRECT (1/1)
        new_sel = [0,1]
    # if previous Weak Correlator
    # condition to move to Weak Non-Correlator
    elif (prev_sel == [0,1] and (mlocal == CORRECT and  mglobal == WRONG)):
        new_sel = [1,0]
    
    # if previous Weak Non-Correlator
    # all conditions to stay in Weak Non-Correlator
    elif ((prev_sel == [1,0] and
        ((mlocal == WRONG and mglobal == WRONG) or # if both are WRONG (0/0)
        (mlocal == CORRECT and mglobal == CORRECT)))):  # if both are CORRECT (1/1)
        new_sel = [1,0]
    # if previous Weak Non-Correlator
    # condition to move to Strong Non-Correlator
    elif (prev_sel == [1,0] and (mlocal == CORRECT and  mglobal == WRONG)):
        new_sel = [1,1]
        
    # if previous Strong Non-Correlator
    # all conditions to stay in Strong Non-Correlator
    elif (((prev_sel == [1,1]) and
        ((mlocal == WRONG and mglobal == WRONG) or # if both are WRONG (0/0)
        (mlocal == CORRECT and mglobal == WRONG)) or # if local is WRONG and global is CORRECT (0/1)
        (mlocal == CORRECT and mglobal == CORRECT))):  # if both are CORRECT (1/1)
        
        new_sel = [1,0]
    # if previous Strong Non-Correlator
    # condition to move to Weak Non-Correlator
    elif ((prev_sel == [1,1]) and (mlocal == WRONG and  mglobal == CORRECT)):
        new_sel = [1,0]

    # now we only have transitions to Weak Correlator and then to Strong Correlator left

    # if previous Weak Non-Correlator
    # condition to move to Weak Correlator
    elif ((prev_sel == [1,0]) and (mlocal == WRONG and  mglobal == CORRECT)):
        new_sel = [0,1]

    # if previous Weak Correlator
    # condition to move to Strong Correlator
    elif ((prev_sel == [0,1]) and (mlocal == WRONG and  mglobal == CORRECT)):
        new_sel = [0,0]

    return new_sel

def global_predictor(ent, h_pc, gl_hist, tak_ntak, tarpc=None, check=None, want_stats=True):
    if gl_hist == [0,0]:
        if check == True:
            chk = check_correct(pred=btb[ent]["g00"], actualt_nt=tak_ntak, ent=ent, tarpc=tarpc)
            if (chk == CORRECT) and (want_stats == True):
                stats["correct_pred"] += 1
            elif want_stats == True:
                stats["wrong_pred"] += 1
        pred = update_pred(prev_pred=btb[ent]["g00"], t_nt=tak_ntak)
        if tarpc == None:
            update_BTB(ent, pc=h_pc, g00=pred)
        else:
            update_BTB(ent, pc=h_pc, tpc=tarpc, g00=pred)
    elif gl_hist == [0,1]:
        if check == True:
            chk = check_correct(pred=btb[ent]["g01"], actualt_nt=tak_ntak, ent=ent, tarpc=tarpc)
            if (chk == CORRECT) and (want_stats == True):
                stats["correct_pred"] += 1
            elif want_stats == True:
                stats["wrong_pred"] += 1
        pred = update_pred(prev_pred=btb[ent]["g01"], t_nt=tak_ntak)
        if tarpc == None:
            update_BTB(ent, pc=h_pc, g00=pred)
        else:
            update_BTB(ent, pc=h_pc, tpc=tarpc, g00=pred)
    elif gl_hist == [1,0]:
        if check == True:
            chk = check_correct(pred=btb[ent]["g10"], actualt_nt=tak_ntak, ent=ent, tarpc=tarpc)
            if (chk == CORRECT) and (want_stats == True):
                stats["correct_pred"] += 1
            elif want_stats == True:
                stats["wrong_pred"] += 1
        pred = update_pred(prev_pred=btb[ent]["g10"], t_nt=tak_ntak)
        if tarpc == None:
            update_BTB(ent, pc=h_pc, g00=pred)
        else:
            update_BTB(ent, pc=h_pc, tpc=tarpc, g00=pred)
    elif gl_hist == [1,1]:
        if check == True:
            chk = check_correct(pred=btb[ent]["g11"], actualt_nt=tak_ntak, ent=ent, tarpc=tarpc)
            if (chk == CORRECT) and (want_stats == True):
                stats["correct_pred"] += 1
            elif want_stats == True:
                stats["wrong_pred"] += 1
        pred = update_pred(prev_pred=btb[ent]["g11"], t_nt=tak_ntak)
        if tarpc == None:
            update_BTB(ent, pc=h_pc, g00=pred)
        else:
            update_BTB(ent, pc=h_pc, tpc=tarpc, g00=pred)

    # only return check if required
    if check == True:
        return chk

def check_collision(ent, curpc):
    if ent in btb:
        if curpc != btb[ent]["pc"]:
            # found a collision
            stats["collisions"] += 1

def check_correct(pred, actualt_nt, ent=None, tarpc=None):
    if pred[0] == TAKEN and actualt_nt == TAKEN:
        if btb[ent]["tpc"] == tarpc:
            return CORRECT
        else:
            return WRONG
    elif pred[0] == TAKEN and actualt_nt == NOT_TAKEN:
        return WRONG
    elif pred[0] == NOT_TAKEN and actualt_nt == TAKEN:
        return WRONG
    elif pred[0] == NOT_TAKEN and actualt_nt == NOT_TAKEN:
        return CORRECT

def check_wrong_address(ent, currpc, actualtpc):
    tpc_in_btb = btb[ent]["tpc"]
    if  (actualtpc != tpc_in_btb) and (actualtpc != currpc+4):
        wrong_addresses[actualtpc] = tpc_in_btb

####### M A I N #####################
def btb_main(m_type, m_codefile, init_local=[1,1], init_global=[1,1], init_selector=[1,0]):
    flush_data()
    with open(m_codefile, "r") as f:
        code = f.readlines()

    # strip out \n newline characters
    code = [x.strip() for x in code]

    for i in range(0, len(code)-2):
        hex_pc_plus1 = code[i+1]
        pc_plus1 = int(code[i+1], 16)
        hex_pc = code[i]
        pc = int(code[i], 16)
        # compute the entry number in BTB
        entry = get_entry_BTB(hex_pc)

        if pc_plus1 - pc == 4:
            # NOT a Branch but if pc in BTB we have NOT TAKEN it
            if in_BTB(entry, pc=hex_pc) == True:
                stats["hits"] += 1
                if m_type == "local":
                    # we know that branch was not taken
                    chk = check_correct(btb[entry]["local_pred"], NOT_TAKEN, ent=entry, tarpc=None)
                    if chk == CORRECT:
                        stats["correct_pred"] += 1
                    else:
                        stats["wrong_pred"] += 1
                    pred = update_pred(prev_pred=btb[entry]["local_pred"], t_nt=NOT_TAKEN)
                    update_BTB(entry, pc=hex_pc, local_pred=pred)
                elif m_type == "global":
                    # we know that branch was not taken
                    # don't update target pc
                    global_predictor(entry, hex_pc, global_hist, NOT_TAKEN, tarpc=None, check=True)
                    # we didn't take the branch so update history
                    update_global_hist(NOT_TAKEN)
                elif m_type == "tournament":
                    # stats["wrong_pred"] += 1
                    # if 1st bit of selector is 1 means use Non-Correlator i.e. local
                    if btb[entry]["sel"][0] == 1:
                        # update local prediction
                        chk_local = check_correct(btb[entry]["local_pred"], NOT_TAKEN, ent=entry, tarpc=None)
                        # update prediction according to state machine
                        if chk_local == CORRECT:
                            stats["correct_pred"] += 1
                        else:
                            stats["wrong_pred"] += 1
                        pred = update_pred(prev_pred=btb[entry]["local_pred"], t_nt=NOT_TAKEN)
                        update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=pred)
                        # update global prediction, we'll check if our prediction is correct but don't update stats
                        chk_global = global_predictor(entry, hex_pc, global_hist, NOT_TAKEN, tarpc=None,
                                                                                        check=True,
                                                                                        want_stats=False)
                        # chk_global = CORRECT


                        # update selector, pass in if local/global prediction were correct or not
                        new_sel = update_selector(btb[entry]["sel"], chk_local, chk_global)
                        update_BTB(entry, sel=new_sel)
                    # 0 means use Correlator i.e. global
                    elif btb[entry]["sel"][0] == 0:
                        # update local prediction
                        chk_local = check_correct(btb[entry]["local_pred"], NOT_TAKEN, ent=entry, tarpc=None)
                        # update prediction according to state machine
                        pred = update_pred(prev_pred=btb[entry]["local_pred"], t_nt=NOT_TAKEN)
                        update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=pred)
                        # update global prediction, we'll check if our prediction is correct and we want stats
                        chk_global = global_predictor(entry, hex_pc, global_hist, NOT_TAKEN, tarpc=None,
                                                                                        check=True,
                                                                                        want_stats=True)
                        # chk_global = CORRECT
                        # stats["wrong_pred"] += 1
                        # update selector, pass in if local/global prediction were correct or not
                        new_sel = update_selector(btb[entry]["sel"], chk_local, chk_global)
                        update_BTB(entry, sel=new_sel)
                        
                    update_global_hist(NOT_TAKEN)
        else:
            # FOUND a Branch hence TAKEN
            logging.warning("FOUND a Branch for PC:{}".format(code[i]))
            
            # see if PC exists in current BTB
            if in_BTB(entry, pc=hex_pc) == True:
                stats["hits"] += 1
                # TODO?: add functionality to see if the target PC is same as in BTB
                # if not then update BTB target address to the new
                # THIS IS ALREADY BEING DONE as we update target PC every iteration
                # NOTE: the arguments provided here become the table columns in BTB
                # e.g. g00 is column in BTB once we update BTB with it
                check_wrong_address(entry, pc, pc_plus1)
                if m_type == "local":
                    chk = check_correct(btb[entry]["local_pred"], TAKEN, ent=entry, tarpc=hex_pc_plus1)
                    if chk == CORRECT:
                        stats["correct_pred"] += 1
                    else:
                        stats["wrong_pred"] += 1
                    # update prediction according to state machine
                    pred = update_pred(prev_pred=btb[entry]["local_pred"], t_nt=TAKEN)
                    update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=pred)

                elif m_type == "global":
                    global_predictor(entry, hex_pc, global_hist, TAKEN, tarpc=hex_pc_plus1, check=True)
                    update_global_hist(TAKEN)

                elif m_type == "tournament":
                    # if 1st bit of selector is 1 means use Non-Correlator i.e. local
                    if btb[entry]["sel"][0] == 1:
                        # update local prediction
                        chk_local = check_correct(btb[entry]["local_pred"], TAKEN, ent=entry, tarpc=hex_pc_plus1)
                        if chk_local == CORRECT:
                            stats["correct_pred"] += 1
                        else:
                            stats["wrong_pred"] += 1
                        # update prediction according to state machine
                        pred = update_pred(prev_pred=btb[entry]["local_pred"], t_nt=TAKEN)
                        update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=pred)
                        # update global prediction, we'll check if our prediction is correct but don't update stats
                        chk_global = global_predictor(entry, hex_pc, global_hist, TAKEN, tarpc=hex_pc_plus1,
                                                                                        check=True,
                                                                                        want_stats=False)
                        # update selector, pass in if local/global prediction were correct or not
                        new_sel = update_selector(btb[entry]["sel"], chk_local, chk_global)
                        update_BTB(entry, sel=new_sel)
                    # 0 means use Correlator i.e. global
                    elif btb[entry]["sel"][0] == 0:
                        # update local prediction
                        chk_local = check_correct(btb[entry]["local_pred"], TAKEN, ent=entry, tarpc=hex_pc_plus1)
                        # update prediction according to state machine

                        pred = update_pred(prev_pred=btb[entry]["local_pred"], t_nt=TAKEN)
                        update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=pred)
                        # update global prediction, we'll check if our prediction is correct and we want stats
                        chk_global = global_predictor(entry, hex_pc, global_hist, TAKEN, tarpc=hex_pc_plus1,
                                                                                        check=True,
                                                                                        want_stats=True)
                        # update selector, pass in if local/global prediction were correct or not
                        new_sel = update_selector(btb[entry]["sel"], chk_local, chk_global)
                        update_BTB(entry, sel=new_sel)

                    update_global_hist(TAKEN)

            else: # Branch TAKEN not in BTB
                if m_type == "local":
                    # this is a TAKEN branch which was not in BTB hence miss
                    stats["misses"] += 1
                    # by default we'll assume Strong Taken
                    update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=init_local)
                    # update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=[1, 0])

                elif m_type == "global":
                    # this is a TAKEN branch which was not in BTB hence miss
                    stats["misses"] += 1
                    # by default we'll assume Strong Taken for all columns
                    update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1,
                                g00=init_global, g01=init_global, g10=init_global, g11=init_global)
                    # update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1,
                    #            g00=[1, 0], g01=[1, 0], g10=[1, 0], g11=[1, 0])

                    # update global history
                    update_global_hist(TAKEN)
                elif m_type == "tournament":
                    # by default we'll assume Strong Taken for all columns
                    # and Weak Non-Correlator i.e. local
                    update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=init_local,
                                g00=init_global, g01=init_global, g10=init_global, g11=init_global,
                                sel=init_selector)
                    # update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=[1,0],
                    #             g00=[1,0], g01=[1,0], g10=[1,0], g11=[1,0],
                    #             sel=[1,0])
                    # update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=[1,1],
                    #             g00=[1,1], g01=[1,1], g10=[1,1], g11=[1,1],
                    #             sel=[0,1])
                    # update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=[1,0],
                    #             g00=[1,0], g01=[1,0], g10=[1,0], g11=[1,0],
                    #             sel=[0,1])

                    update_global_hist(TAKEN)
                    # this is a TAKEN branch which was not in BTB hence miss
                    stats["misses"] += 1

if __name__ == "__main__": 
    print("Executed when invoked directly")
    parser = argparse.ArgumentParser()
    parser.add_argument("--codefile", help="provide the file path to file containing opcodes")
    parser.add_argument("--type", help="local, global or tournament")
    args = parser.parse_args()

    report_type = args.type
    report_codefile = args.codefile
    # by default we'll assume Strong Taken for all columns
    # and Weak Non-Correlator i.e. start with local predictor
    btb_main(report_type, report_codefile)

    # printing final state of BTB
    # pass in "local", "global" or "tournament"
    print_BTB(report_type, sort=True)
    print_stats(stats=stats)
    print_wrong_addresses(wrong_addresses)
