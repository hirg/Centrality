#!/bin/bash
#SBATCH --nodes=1
#SBATCH --time=20:00:00
#SBATCH --mem-per-cpu=4G
#SBATCH --output=jb0.out
#SBATCH --job-name="jb0filter"

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc491
export X509_USER_PROXY=/home/tuos/x509up_u126986
#cd /home/tuos/reco2AOD/CMSSW_7_4_0_pre8/src/slurm
cd /scratch/tuos/temp/cmssw/CMSSW_7_5_0/src/ppreco/jobs/pbpb/filter/v1/cent2/jb0
eval `scramv1 runtime -sh`

cmsRun get_FilteredEvents.py

exit 0

