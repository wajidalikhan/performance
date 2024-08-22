#/tmp/x509up_u31059i                                                                                                                                                                                         
#export X509_USER_PROXY=/afs/cern.ch/user/a/abenecke/myProxy
source /cvmfs/cms.cern.ch/crab3/crab.sh
voms-proxy-init -rfc -voms cms -valid 192:00


echo "Info: "$PWD
echo "Info: Copying proxy to an area in afs : "$HOME

cp /tmp/x509up_u31059 $HOME
echo "Info: Export the variable X509_USER_PROXY  at: "$HOME/x509up_u31059
export X509_USER_PROXY=/afs/cern.ch/user/w/wajid/x509up_u31059

source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh
source bamboovenv/bin/activate

export JMEVALIDATIONPATH=$(pwd -L)
export PYTHONPATH=${PYTHONPATH}:${JMEVALIDATIONPATH}




#source /cvmfs/cms.cern.ch/crab3/crab.sh
#voms-proxy-init -rfc -voms cms -valid 192:00
#
#source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh
#source bamboovenv/bin/activate
#
#export JMEVALIDATIONPATH=$(pwd -L)
#export PYTHONPATH=${PYTHONPATH}:${JMEVALIDATIONPATH}
