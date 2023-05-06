# jme-validation

Setup based on Bamboo (https://gitlab.cern.ch/cp3-cms/bamboo) to validate JME diliverables

you need to create the file `~/.config/bamboorc`
with the folling information:
```sh
[batch]
backend = slurm

[slurm]
sbatch_additionalOptions = --licenses=cms_storage:3
sbatch_qos = cp3
sbatch_partition = cp3

[das]
sitename = T2_BE_UCL
storageroot = /storage/data/cms
checklocalfiles = no
xrootdredirector = xrootd-cms.infn.it
```

In case you update module, you should reinstall the packages dependencies using:

```sh
pip install --upgrade .
```