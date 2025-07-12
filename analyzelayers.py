#!/usr/bin/env python3


import glob,os,sys
import json
import pandas
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
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

hidden_space2s = np.int64([ settings_content[i]['hidden_space2'] for i in range(nitems) ])
meanfirstthirds = np.array( [ results_content[i]['meanfirstthird'] for i in range(nitems) ])
meanlastthirds = np.array([ results_content[i]['meanlastthird'] for i in range(nitems) ])



plt.plot(hidden_space2s, meanlastthirds,'o')
#plt.ticklabel_format(axis='x', style='sci', scilimits=(0, 0))
for i in range(nitems):
    plt.text(hidden_space2s[i]+0.2, meanlastthirds[i]+0.2, f"{hidden_space2s[i]}", fontsize=8, ha='left', va='bottom')
plt.savefig(os.path.join(thistrial,'meanlastthirds.png'))


plt.close('all')

print(f"Number of items: {nitems}")
print(f"Hidden space 1 values: {len(hidden_space2s)}")
print(f"Mean first thirds: {len(meanfirstthirds)}")

vpdata = [ meanlastthirds[hidden_space2s==i] for i in np.unique(hidden_space2s) ]


plt.violinplot(vpdata, positions=sorted(np.unique(hidden_space2s)), showmeans=True, showmedians=True)
plt.xlabel('hidden_space2')
plt.ylabel('meanlastthird')
plt.title('meanlastthirds vs hidden_space2,')
figfile = os.path.join(thistrial, 'meanlastthirds_violin.png')
plt.savefig(figfile)

os.system(f'eog {figfile}  &')

print(settings_content)
print(results_content)
