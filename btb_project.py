import sys
import logging
import argparse

####### I N I T #####################
btb = dict()

TAKEN = 1
NOT_TAKEN = 0

stats_local = {
    "hits": 0,
    "misses":	0,
	"right_pred": 0,
	"wrong_pred": 0,
	"wrong_address": 0,
	"collisions": 0
}

global_hist = [0,0]

stats_global = {
    "hits": 0,
    "misses":	0,
	"right_pred": 0,
	"wrong_pred": 0,
	"wrong_address": 0,
	"collisions": 0
}

stats_tournament = {
    "hits": 0,
    "misses":	0,
	"right_pred": 0,
	"wrong_pred": 0,
	"wrong_address": 0,
	"collisions": 0
}

logging.basicConfig(filename='cpts561_log.log', filemode='w', level=logging.DEBUG)

parser = argparse.ArgumentParser()
parser.add_argument("--codefile", help="provide the file path to file containing opcodes")
parser.add_argument("--type", help="local, global or tournament")
args = parser.parse_args()

####### F U N C T I O N S #####################
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
            btb[entry][key] = val
    else:
        # create new entry in BTB
        temp_btb = dict()
        for key, val in kwargs.items():
            # print("key:{}, val:{}".format(key, val))
            temp_btb[key] = val

        btb[entry % 1024] = temp_btb

def print_stats(stats):
    print("hits:{} -- misses:{} -- right predictions:{} -- wrong predictions:{}".format(
                                                    stats["hits"],
                                                    stats["misses"],
                                                    stats["right_pred"],
                                                    stats["wrong_pred"]))
        
def print_BTB(ptype, sort=False):
    if sort == True:
        # TODO: this is broken - fix if needed
        # sorted_btb = [val for (key, val) in sorted(btb.items())]
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
                print("{} --- PC {} - targetPC {} - g00 {} - g01 {} - g01 {} - g11 {}".format(entry,
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
                print("{} --- PC {} - targetPC {} - g00 {} - g01 {} - g01 {} - g11 {}".format(entry,
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
                if args.type == "local":
                    logging.debug("BTB entry {} --- PC {} - targetPC {} - local_pred {}".
                                                            format(entry, 
                                                            btb[entry]["pc"], 
                                                            btb[entry]["tpc"],
                                                            btb[entry]["local_pred"]))
                elif args.type == "global":
                    logging.debug("{} --- PC {} - targetPC {} - g00 {} - g01 {} - g01 {} - g11 {}".format(entry,
                                                            btb[entry]["pc"], 
                                                            btb[entry]["tpc"],
                                                            btb[entry]["g00"],
                                                            btb[entry]["g01"],
                                                            btb[entry]["g10"],
                                                            btb[entry]["g11"]))
                return True
            else:
                logging.debug("PC {} not in BTB, compared to {}".format(
                                                                pc,
                                                                btb[entry]["pc"]))
                return False
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

####### M A I N #####################
with open(args.codefile, "r") as f:
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
            # take the Target PC value from BTB instead of pc+4
            # another solution is to not updated the BTB! just update the prediction
            # keep = btb[entry % 1024]["tpc"]
            if args.type == "local":
                # we know that branch was not taken
                stats_local["wrong_pred"] += 1
                pred = update_pred(prev_pred=btb[entry]["local_pred"], t_nt=NOT_TAKEN)
                update_BTB(entry, pc=hex_pc, local_pred=pred)
            elif args.type == "global":
                # we know that branch was not taken
                stats_global["wrong_pred"] += 1
                if global_hist == [0,0]:
                    pred = update_pred(prev_pred=btb[entry]["g00"], t_nt=NOT_TAKEN)
                    update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, g00=pred)
                elif global_hist == [0,1]:
                    pred = update_pred(prev_pred=btb[entry]["g01"], t_nt=NOT_TAKEN)
                    update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, g01=pred)
                elif global_hist == [1,0]:
                    pred = update_pred(prev_pred=btb[entry]["g10"], t_nt=NOT_TAKEN)
                    update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, g10=pred)
                elif global_hist == [1,1]:
                    pred = update_pred(prev_pred=btb[entry]["g11"], t_nt=NOT_TAKEN)
                    update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, g11=pred)
                # we didn't take the branch so update history
                update_global_hist(NOT_TAKEN)
    else:
        # FOUND a Branch hence TAKEN
        logging.warning("FOUND a Branch for PC:{}".format(code[i]))
        
        # see if PC exists in current BTB
        if in_BTB(entry, pc=hex_pc) == True:
            # TODO?: add functionality to see if the target PC is same as in BTB
            # if not then update BTB target address to the new
            # THIS IS ALREADY BEING DONE as we update target PC every iteration
            # NOTE: the arguments provided here become the table columns in BTB
            # e.g. g00 is column in BTB once we update BTB with it
            if args.type == "local":
                # update stats
                stats_local["hits"] += 1
                # see if target PC in BTB is same as the next PC
                if btb[entry]["tpc"] == hex_pc_plus1:
                    # correct prediction!
                    stats_local["right_pred"] += 1
                else:
                    stats_local["wrong_pred"] += 1
                # update prediction according to state machine
                pred = update_pred(prev_pred=btb[entry]["local_pred"], t_nt=TAKEN)
                # we know the Target PC is the next instruction hence code[i+1]
                update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=pred)
            elif args.type == "global":
                # update stats
                stats_global["hits"] += 1
                # see if target PC in BTB is same as the next PC
                if btb[entry]["tpc"] == hex_pc_plus1:
                    # correct prediction!
                    stats_global["right_pred"] += 1
                else:
                    stats_global["wrong_pred"] += 1
                if global_hist == [0,0]:
                    pred = update_pred(prev_pred=btb[entry]["g00"], t_nt=TAKEN)
                    update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, g00=pred)
                elif global_hist == [0,1]:
                    pred = update_pred(prev_pred=btb[entry]["g01"], t_nt=TAKEN)
                    update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, g01=pred)
                elif global_hist == [1,0]:
                    pred = update_pred(prev_pred=btb[entry]["g10"], t_nt=TAKEN)
                    update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, g10=pred)
                elif global_hist == [1,1]:
                    pred = update_pred(prev_pred=btb[entry]["g11"], t_nt=TAKEN)
                    update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, g11=pred)
                # update global history
                update_global_hist(TAKEN)
            # elif args.type == "tournament":

        else:
            if args.type == "local":
                # by default we'll assume Strong Taken
                update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, local_pred=[1,1])
                # this is a TAKEN branch which was not in BTB hence miss
                stats_local["misses"] += 1

            elif args.type == "global":
                # by default we'll assume Strong Taken for all columns
                update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, g00=[1,1])
                update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, g01=[1,1])
                update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, g10=[1,1])
                update_BTB(entry, pc=hex_pc, tpc=hex_pc_plus1, g11=[1,1])
                # this is a TAKEN branch which was not in BTB hence miss
                stats_global["misses"] += 1

# printing final state of BTB
# pass in "local", "global" or "tournament"
print_BTB(args.type, sort=True)
# pass in the required stats dictionary
if args.type == "local":
    print_stats(stats=stats_local)
elif args.type == "global":
    print_stats(stats=stats_global)
elif args.type == "tournament":
    print_stats(stats=stats_tournament)