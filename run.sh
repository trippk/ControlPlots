#!/bin/bash

source /afs/cern.ch/sw/lcg/contrib/gcc/4.8/x86_64-slc6/setup.sh
. /etc/profile.d/modules.sh
module use -a /afs/desy.de/group/cms/modulefiles/
module load root/5.34

./makeControlPlots.py