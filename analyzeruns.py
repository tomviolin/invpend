#!/usr/bin/env python3


import glob,os,sys
import json
import pandas
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')

# get list of trials
trials = sorted(glob.glob('trials/trial_*'))
numback = 0
if len(sys.argv) > 1:
    numback = int(sys.argv[1])

thistrial = trials[-1-numback]
print(f"trial selected = {thistrial}")
settings_array=sorted(glob.glob(f'{thistrial}/*/settings.json'))
results_array=sorted(glob.glob(f'{thistrial}/*/results.json'))

settings_content = [ json.load(open(sfile,'r')) for sfile in settings_array]
results_content = [ json.load(open(rfile,'r')) for rfile in results_array]

nitems = min(len(settings_content),len(results_content))

settings_content = settings_content[:nitems]
results_content = results_content[:nitems]

learning_rates = [ settings_content[i]['learning_rate'] for i in range(nitems) ]
meanfirstthirds = [ results_content[i]['meanfirstthird'] for i in range(nitems) ]
meanlastthirds = [ results_content[i]['meanlastthird'] for i in range(nitems) ]

print(f"len(learning_rates)={len(learning_rates)}")
print(f"len(meanfirstthirds)={len(meanfirstthirds)}")
print(f"len(meanlastthirds)={len(meanlastthirds)}")

meanimprovement = [ meanlastthirds[i] - meanfirstthirds[i] for i in range(nitems) ]

plt.plot(learning_rates, meanimprovement,'-o')
plt.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
plt.savefig('meanimprovement.png')
os.system('eog meanimprovement.png &')

print(settings_content)
print(results_content)
