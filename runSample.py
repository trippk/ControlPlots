#!/usr/bin/python
import sys
import os
from glob import glob
from sys import exit
'''
# load root in batch mode
sysarg = sys.argv
sys.argv = ['-b']
from ROOT import gROOT
from ROOT import TFile
sys.argv = sysarg
'''

def help():
    print 'First argument analysis:'
    print './runreader.py SampleDir (with tree,tth etc. structure)'
    sys.exit(0)

def GetNevents(loc):
    # get full number of events generated
    EvtFile = open(loc+"ttHLepSkimmer/events.txt", "r")

    for line in EvtFile.readlines():
        if 'all events' in line:
            evts = line.split()[2]
            break

    return float(evts)

# Get sample directory
if len(sys.argv) > 1:
    sampDir = sys.argv[1]
else:
    help()

# Settings
treename = 'treeProducerSusySingleLepton'
#exe = 'TreeAnalyzer_SingleEl.exe'
exe = 'TreeAnalyzer_controlPlots.exe'

# Get current script dir
pyDir = sys.argv[0]
cwd = os.path.dirname(pyDir)

# get relative path
exe = cwd+'/../'+exe

# Remove the trailing / : rstrip('//')
sample = os.path.basename(sampDir.rstrip('//'))

# get scenario MC/Data
if 'MC' in sampDir: scene = 'MC'
else: scene = 'Data'

# weight, lumi, cross section, number of events
# Calculate number of events
lumi = 1000 #pb-1
entries = GetNevents(sampDir+'/')
weight = lumi/entries
print sampDir, 'has', entries, 'entries for sample', scene+'_'+sample, weight

# NB! weight is lumi/entries
fileName = sampDir+'/'+treename+'/ '+str(weight)+' '

print([exe, fileName,scene+'_'+sample])
print ' !!!!!!!: ', exe+" "+fileName+" "+scene+'_'+sample
os.system(exe+" "+fileName+" "+scene+'_'+sample)
