# jme-validation

Framework based on Bamboo (https://gitlab.cern.ch/cp3-cms/bamboo) to validate JME deliverables.

## Installation
In order to install the framework, first git-clone:
```
git clone https://github.com/cms-jet/jme-validation
```
Then, run the installation script:
```
source install.sh

```
After installation, a few changes to the bamboo code are neeed. These changes will soon be implemented directly inside the installation script. For the time being, you can implement them using the `sed` command. Known changes needed:
```
     sed -i 's/"Rho_fixedGridRhoFastjetAll"/"Rho"/g' bamboo/bamboo/analysisutils.py
     sed -i 's/"Rho_fixedGridRhoFastjetAll"/"Rho"/g' bamboovenv/lib/python3.9/site-packages/CMSJMECalculators/utils.py
     sed -i 's/JRDatabase/jme-validation/g' bamboo/bamboo/analysisutils.py
     sed -i 's/JECDatabase/jme-validation/g' bamboo/bamboo/analysisutils.py
     sed -i '/cms-jet\/jme-validation/s/$/ branch="main",/' bamboo/bamboo/analysisutils.py
     sed -i 's/heads\/master"/heads\/"+self.branch/g' bamboovenv/lib/python3.9/site-packages/CMSJMECalculators/jetdatabasecache.py
     sed -i 's/idxs=defCache(self.rng)/idxs=defCache(self.rng).replace("IndexRange<std::size_t>{","IndexRange<std::size_t>{static_cast<unsigned long>(").replace("}",")}")/g' bamboo/bamboo/treeoperations.py

```

Every time you change bamboo-related code,  you have to reinstall the packages dependencies by doing
```sh
pip install --upgrade .
```
or using the bash script:
```sh
source recompile.sh
```

Finally, inside the `jme-validation` main folder, you need to create a file called `bamboo.init` with the following content:
```sh
[batch]
backend = htcondor

[htcondor]
jobflavour = "longlunch"

[das]
sitename = T2_CH_CERN
storageroot = /eos/cms
xrootdredirector = cms-xrd-global.cern.ch

```

## Running the framework
You can first perform a test run. Do:
```
 ./macros/steer.py -c -t
```
If everything looks good, you can submit condor jobs:
```
./macros/steer.py -c -s
```
Finally, you can make plots:
```
./macros/steer.py -p
```
