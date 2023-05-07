# jme-validation

Setup based on Bamboo (https://gitlab.cern.ch/cp3-cms/bamboo) to validate JME diliverables

you need to create the file `bamboo.ini`
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