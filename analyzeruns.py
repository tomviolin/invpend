#!/usr/bin/env python3

import glob,os,sys
import json
import pandas
import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
matplotlib.use('gtk4agg')
import numpy as np
from numpy import log,exp,sqrt,mean,median
from matplotlib.colors import TABLEAU_COLORS, same_color
prop_cycle = plt.rcParams['axes.prop_cycle']

cpal = prop_cycle.by_key()['color']

tmp=cpal[0]
cpal[0]=cpal[1]
cpal[1]=tmp

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

learning_rates = np.array([ settings_content[i]['learning_rate'] for i in range(nitems) ])
meanfirstthirds = np.array([ results_content[i]['meanfirstthird'] for i in range(nitems) ])
meanlastthirds = np.array([ results_content[i]['meanlastthird'] for i in range(nitems) ])

print(f"len(learning_rates)={len(learning_rates)}")
print(f"len(meanfirstthirds)={len(meanfirstthirds)}")
print(f"len(meanlastthirds)={len(meanlastthirds)}")


meanimprovement = [ meanlastthirds[i] - meanfirstthirds[i] for i in range(nitems) ]

plt.figure(dpi=300)


# divide x axis within xlim into equal parts.
N_BINS = 20
BINSWIDE = 3 # must be odd
bounds = np.logspace(log(min(learning_rates))/log(10),log(max(learning_rates))/log(10),N_BINS+1)

means2   = []
medians2 = []

stdev2 = []
qt25 = []
qt75 = []


plt.plot(learning_rates, meanlastthirds, '.',label='last 1/3',ms=10, color=cpal[4]+'90', mec=cpal[4]+'00')


for i in range(N_BINS):
    lo_index = max(i-(BINSWIDE//2),0)
    hi_index = min(i+(BINSWIDE//2+1),N_BINS)
    sample_filter = np.uint64(np.where(np.logical_and(
        learning_rates >= bounds[lo_index],
        learning_rates < bounds[hi_index]
    ))[0])

    print(sample_filter.dtype)
    means2.append  (np.mean    (meanlastthirds[sample_filter]))
    medians2.append(np.median  (meanlastthirds[sample_filter]))
    stdev2.append  (np.std     (meanlastthirds[sample_filter]))
    qt25.append    (np.quantile(meanlastthirds[sample_filter],0.25))
    qt75.append    (np.quantile(meanlastthirds[sample_filter],0.75))

means2 = np.array(means2)
medians2 = np.array(medians2)
stdev2 = np.array(stdev2)
qt25 = np.array(qt25)
qt75 = np.array(qt75)
xcoords = [ (bounds[i+1]+bounds[i])/2.0 for i in range(N_BINS)]


plt.fill_between(xcoords,means2-stdev2,means2+stdev2,color=cpal[1]+'30')
plt.fill_between(xcoords,qt25,qt75,color=cpal[0]+'30' )


plt.plot(xcoords,means2, '--', color=cpal[1])
plt.plot(xcoords,medians2, ':', color=cpal[0])
plt.xscale('log')
#plt.ticklabel_format(axis='x')
plt.legend()
plt.title(f'model reward by learning rate')
graphfile = os.path.join(thistrial,'meanimprovement.svg')
plt.savefig(graphfile)
os.system('eog "' + graphfile + '" &')

print(settings_content)
print(results_content)
