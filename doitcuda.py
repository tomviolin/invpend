#!/usr/bin/env python3
import os,sys
import numpy as np
import json
import time
import signal
import sys

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


try:

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

    for lr in np.arange(0.0001, 0.0099, 0.000005):
        rundatestamp = datetime.now().strftime('%Y_%m%d_%H%M%S')
        rundir = os.path.join(projdir, 'gpu_trials',f'trial_{trialdatestamp}', f'lr_{rundatestamp}_{lr:0.6f}')
        if not os.path.exists(rundir):
            os.makedirs(rundir,exist_ok=True)
        print(f"Run directory created: {rundir}")

        settings = { 
                    "learning_rate": lr, 
                    "seed": np.random.randint(0, 10000),
                    "total_num_episodes": 100
        } 


        settings_file = os.path.join(rundir,"settings.json")
        with open(settings_file,"w") as f:
            f.write(json.dumps(settings,indent=2))
        time.sleep(1)        
        os.system(f'sleep 0.1; python3 reinforce_invpend_gym_v26_cuda.py {settings_file}')

    """
    if not os.path.exists(logdir):
        os.makedirs(logdir, exist_ok=True)

    print(f"Log directory created: {logdir}")
    """

except KeyboardInterrupt as e:
    print("KeyboardInterrupt caught. Exiting gracefully.")
    sys.exit(0) 


