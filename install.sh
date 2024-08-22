source /cvmfs/sft.cern.ch/lcg/views/LCG_105/x86_64-el9-gcc11-opt/setup.sh
python -m venv bamboovenv
source bamboovenv/bin/activate
# clone and install bamboo
git clone -o upstream https://gitlab.cern.ch/cms-analysis/general/bamboo.git
pip install ./bamboo
# clone and install correctionlib, CMSJMECalculators, plotIt
pip install --no-binary=correctionlib correctionlib
pip install git+https://gitlab.cern.ch/cms-analysis/general/CMSJMECalculators.git
git clone -o upstream https://github.com/cp3-llbb/plotIt.git
mkdir build-plotit
cd build-plotit
cmake -DCMAKE_INSTALL_PREFIX=$VIRTUAL_ENV ../plotIt
make -j2 install
cd -
