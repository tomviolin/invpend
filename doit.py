#!/usr/bin/env python3
import os,sys
import numpy as np
import json
import time

# establish log file path based on current date and time

# directory structure of log run files
# trials/trial_{dt}/lr_{rdt}_0.000090/
# trials/trial_{dt}/lr_{rdt}_0.000091/
# trials/trial_{dt}/lr_{rdt}_0.000092/
# 
from datetime import datetime
trialdatestamp = datetime.now().strftime('%Y_%m%d_%H%M%S')
print(f"Current date and time: {trialdatestamp}")

projdir = os.path.dirname(os.path.abspath(__file__))

if len(sys.argv) > 1:
    num_slots = int(sys.argv[1])
else:
    num_slots = 1

print(f"Number of slots: {num_slots}")
# divvy up the learning rates across the slots

slotcmds = [""] * num_slots

trialdir = os.path.join(projdir, 'trials', f'trial_{trialdatestamp}')
procno = 0

logscale = True

# construct list of learning rates
if logscale:
    lr_list = np.pow(10.0, np.arange(-10, -5, 0.0001))
else:
    lr_list = np.arange(0.000301, 0.000901, 0.000001)

#for lr in :
for lr in lr_list:
    slotno = procno % num_slots
    rundatestamp = datetime.now().strftime('%Y_%m%d_%H%M%S')
    rundir = os.path.join(trialdir, f'lr_{procno:04d}_{lr:0.6f}')

    if not os.path.exists(rundir):
        os.makedirs(rundir,exist_ok=True)
    print(f"Run directory created: {rundir}")

    settings = { 
                "learning_rate": lr, 
                "total_num_episodes": 500,
                "hidden_space1": 20,
                "hidden_space2": 20,
                "render_mode": "none",
                "xscale":"log" if logscale else "lin"
    } 

    settings_file = os.path.join(rundir,"settings.json")
    with open(settings_file,"w") as f:
        f.write(json.dumps(settings,indent=2))
    
    slotcmds[slotno] += f'python3 rein.py {settings_file} > {rundir}/log.txt 2>&1\n'

    procno += 1

logdir = os.path.join(trialdir, 'logs')
# run directories and settings files are ready
procno = 0
for cmd in slotcmds:
    batchfile = os.path.join(logdir, f'slot_{procno:02d}.sh')
    if not os.path.exists(logdir):
        os.makedirs(logdir, exist_ok=True)
    with open(batchfile, 'w') as f:
        f.write("#!/bin/bash\n")
        f.write(cmd + "\n")
    print(f"$ bash {batchfile} &")
    os.system(f"bash {batchfile} &")
    procno += 1
    time.sleep(.1)
    
"""
if not os.path.exists(logdir):
    os.makedirs(logdir, exist_ok=True)

print(f"Log directory created: {logdir}")
"""

