#!/usr/bin/python
####!/usr/bin/env python
import glob, os, subprocess, time   

cmgTuples_path = '/nfs/dust/cms/group/susy-desy/Run2/MC/CMGtuples/'
path = os.path.normpath(cmgTuples_path)
runSample_dir = '/nfs/dust/cms/user/trippk/dust/TreeAnalyzer_with_noID_180315/CMSSW_7_2_3/src/TreeAnalyzer/CMGToolAna/python/'

oldFiles=[]
newFiles=[]
runFiles=[]

#subprocess.Popen([cmsenv, ... ], cwd=working_directory)
#subprocess.Popen('cmsenv', cwd='/nfs/dust/cms/user/trippk/dust/TreeAnalyzer_with_noID_180315/CMSSW_7_2_3/src/TreeAnalyzer/CMGToolAna/python/')

#subprocess.Popen("cd /nfs/dust/cms/user/trippk/dust/TreeAnalyzer_with_noID_180315/CMSSW_7_2_3/src/TreeAnalyzer/CMGToolAna/python/")
#subprocess.Popen('module use -a /afs/desy.de/group/cms/modulefiles/')
#subprocess.Popen('module load root/5.34')

#subprocess.call('cmsenv', shell=True)
#subprocess.call('cd /afs/desy.de/user/t/trippk/', shell=True)

#subprocess.call('module use -a /afs/desy.de/group/cms/modulefiles/', shell=True)
#subprocess.call('module load root/5.34', shell=True)
#subprocess.call('cd /nfs/dust/cms/user/trippk/dust/TreeAnalyzer_with_noID_180315/CMSSW_7_2_3/src/TreeAnalyzer/CMGToolAna/python/', shell=True)
#subprocess.call('eval `/cvmfs/cms.cern.ch/common/scramv1 runtime -sh`', shell=True)



# list of old files
if os.path.isfile('/nfs/dust/cms/user/trippk/dust/TreeAnalyzer_with_noID_180315/CMSSW_7_2_3/src/TreeAnalyzer/CMGToolAna/python/CMGTuples_list.txt'):
    cmg = open('/nfs/dust/cms/user/trippk/dust/TreeAnalyzer_with_noID_180315/CMSSW_7_2_3/src/TreeAnalyzer/CMGToolAna/python/CMGTuples_list.txt')
    for entry in cmg:
        oldFiles.append(entry)
    cmg.close()
else:
    oldFiles = [0]

# list of new files
# root: directory
# dirs: list of directories inside root
# files: list of files in every root (also besides dirs)
for root,dirs,files in os.walk(path, topdown=True):
    # keep only dirs with a tree.root inside
    if 'treeProducerSusySingleLepton' in root:
        if 'tree.root' in files:
            # argument for runSample.py
            newRoot = root.replace('/treeProducerSusySingleLepton','')
            newFiles.append(newRoot+'\n')

# compare old with new list
for item in newFiles:
    if item not in oldFiles:
        runFiles.append(item)

# write new list to CMGTuples_list.txt
gmc = open('/nfs/dust/cms/user/trippk/dust/TreeAnalyzer_with_noID_180315/CMSSW_7_2_3/src/TreeAnalyzer/CMGToolAna/python/CMGTuples_list.txt','w')
for item in newFiles:
    gmc.write("%s\n" % item)
gmc.close()


# run TreeAnalyzer_controlPlots: write out histos from the tree 
if not runFiles:
    print "nothing to do"
else:
#    os.system('/nfs/dust/cms/user/trippk/dust/TreeAnalyzer_with_noID_180315/CMSSW_7_2_3/src/TreeAnalyzer/CMGToolAna/python/cmsenv')
    for item in runFiles:
        print "item: ", item
        # one or many files
        os.system(runSample_dir+'runSample.py '+item)
    os.system(runSample_dir+'check.py ./')

# run check.py over outPut/


print "finished"




### To Do list:
# 2. which order is in CMGTuples_list.txt ???



"""
                    print 'run on ', root, files[0]
                    os.system('runSample.py '+root)

        else:
            exit(0)

#for sample in runDirs:
#subprocess.call(['runSample.py CMGtuples/Phys14_Iso/WJets/WJetsToLNu_HT100to200/'])


#os.system('runSample.py '+cmgTuples_path+'Phys14_Iso/WJets/WJetsToLNu_HT100to200/')

#! test if root files are not closed yet (so copy process is ongoing)
#! test if a 'makeControlPlots' job is still/already running
# check if ./makeControlPlots.py is not running -> process.py ### don't need that !!!

"""
