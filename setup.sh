source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init -rfc -voms cms -valid 192:00

source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh
source bamboovenv/bin/activate

export JMEVALIDATIONPATH=$(pwd -L)
export PYTHONPATH=${PYTHONPATH}:${JMEVALIDATIONPATH}
