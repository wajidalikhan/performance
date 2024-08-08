# jme-validation

Framework based on [Bamboo](https://gitlab.cern.ch/cp3-cms/bamboo), running on `NanoAOD`, to validate JME deliverables.

## Installation
In order to install the framework, first git-clone:
```
git clone https://github.com/cms-jet/jme-validation
```
Then, run the installation script:
```
source install.sh
```
The script will install Bamboo, [plotit](https://github.com/cp3-llbb/plotIt) and [CMSJMECalculators](https://gitlab.cern.ch/cms-analysis/general/CMSJMECalculators) inside a python virtual environment. \

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
To have the framework run, first source everything you need by doing
```
source setup.sh
```
We currently have two modules (corresponding to different selections) that can be run:
* QCD: used to obtain MC truth corrections;
* DY: used for jet reconstruction efficiency/purity and tau performance plots.

The choice of which module to run can be made by setting the `module` variable inside `/macros/steer.py` accordingly.

You can perform a test run by doing:
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

## Running on custom NanoAODs
The framework can be run either on centrally-produced `NanoAOD` samples or custom ones. In order to produce custom NanoAOD samples that meet most of needs of the JME group, we are currently developing the [JMENano framework](https://gitlab.cern.ch/cms-jetmet/jmenano).
