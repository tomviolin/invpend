#!/usr/bin/env python3
import os,sys
import numpy as np
import json

import signal
import sys
import time

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')


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
lr = 0.0006
nlay1 = 43
for k in range(20):
    for nlay2 in range(10,21,1):
        rundatestamp = datetime.now().strftime('%Y_%m%d_%H%M%S')
        rundir = os.path.join(projdir, 'trials',f'trial_{trialdatestamp}', f'h2_{rundatestamp}_{nlay2:03d}')
        if not os.path.exists(rundir):
            os.makedirs(rundir,exist_ok=True)
        print(f"Run directory created: {rundir}")

        settings = { 
                    "learning_rate": lr, 
                    "seed": np.random.randint(0, 10000),
                    "total_num_episodes": 500,
                    "hidden_space1": nlay1,
                    "hidden_space2": nlay2,
                    "title": f"{nlay2} nodes in hidden layer 2"
        } 


        settings_file = os.path.join(rundir,"settings.json")
        with open(settings_file,"w") as f:
            f.write(json.dumps(settings,indent=2))
        time.sleep(0.1)  # small delay to give ^Cs a chance
        system_cline = (f'sleep 0.1; python3 reinforce_invpend_gym_v26.py {settings_file}')
        print(f"\x1b[32m]>>>\x1b[0m {system_cline}")
        os.system(f'sleep 0.1; python3 reinforce_invpend_gym_v26.py {settings_file}')

"""
if not os.path.exists(logdir):
    os.makedirs(logdir, exist_ok=True)

print(f"Log directory created: {logdir}")
"""

