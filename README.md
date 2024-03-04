# jme-validation

Setup based on Bamboo (https://gitlab.cern.ch/cp3-cms/bamboo) to validate JME diliverables

you need to create the file `bamboo.init`
with the folling information:
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

In case you update module, you should reinstall the packages dependencies using:

```sh
pip install --upgrade .
```

or use the bash script:
```sh
source recompile.sh
```

Known changes needed:
    - `sed -i 's/"fixedGridRhoFastjetAll"/"Rho_fixedGridRhoFastjetAll"/g' bamboo/bamboo/analysisutils.py`
    
    - `sed -i 's/JRDatabase/jme-validation/g' bamboo/bamboo/analysisutils.py`
    
    - `sed -i 's/JECDatabase/jme-validation/g' bamboo/bamboo/analysisutils.py`
    
    - `sed -i '/cms-jet\/jme-validation/s/$/ branch="main",/' bamboo/bamboo/analysisutils.py`
    
    - `sed -i 's/heads\/master"/heads\/"+self.branch/g' bamboovenv/lib/python3.9/site-packages/CMSJMECalculators/jetdatabasecache.py`
    
    - `sed -i 's/idxs=defCache(self.rng)/idxs=defCache(self.rng).replace("IndexRange<std::size_t>{","IndexRange<std::size_t>{static_cast<unsigned long>(").replace("}",")}")/g' bamboo/bamboo/treeoperations.py`
