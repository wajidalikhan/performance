import os, subprocess, yaml
from collections import OrderedDict
from printing_utils import green, blue, prettydict

from Constants import Constants

class GenericPath:
    ''' Class container for paths '''
    def __init__(self):
        self.username = os.environ['USER']
        self.jme_path = os.environ['JMEVALIDATIONPATH']
        self.local_path = os.environ['PWD']
        self.config_path = os.path.join(self.jme_path, 'config')
        self.module_path = os.path.join(self.jme_path, 'modules')


class ModuleRunner(GenericPath, Constants):
    ''' Class container for list of objects for particular year '''
    def __init__(self, module, years, runs, campaigns, extraName=None):
        GenericPath.__init__(self)
        self.module = module
        self.module_name = os.path.join(self.module_path, self.module+'Module.py')
        self.output_path = os.path.join(self.jme_path,'outputs', self.module+'Module')
        self.years = years
        self.runs = runs
        self.campaigns = campaigns
        self._unique_name = f'year_{"".join(self.runs)}_{"_".join(self.campaigns.values())}'
        if extraName:
            self._unique_name += '_'+extraName
        self.split_files_in = 100
        print(self)
        Constants.__init__(self)
    
    def get_unique_name(self,year):
        return self._unique_name.replace('year',year)

    def __str__(self):
        print(blue('--> ModuleRunner info:'))
        prettydict(self.__dict__)
        return blue('--> ModuleRunner info: end.')

    def CreateConfigFiles(self):
        for year in self.years:
            era_infos = {year: {'luminosity': self.get_lumi(year,self.runs)}}
            sample_infos = {}
            for ds in self.get_datasets(year,self.runs):
                if not any([x in ds for x in self.modules[self.module]]): continue
                sample_infos[ds] = {
                    'era': year,
                    'group': ds,
                    # 'db': 'das:/TTTo2L2Nu_CP5_13p6TeV_powheg-pythia8/Run3Winter22NanoAOD-122X_mcRun3_2021_realistic_v9-v1/NANOAODSIM',
                    'files': os.path.join(self.jme_path, self.get_files(year=year, campaigns=self.campaigns, dataset=ds)),
                    'type': self.get_type(dataset=ds,year=year),
                    'split': self.split_files_in,
                    }
                if sample_infos[ds]['type']=='mc':
                    sample_infos[ds]['cross-section'] = self.xsec[ds]
                    sample_infos[ds]['generated-events'] = 'genEventSumw'
                else:
                    sample_infos[ds]['group'] = 'data'
            info = {
                'tree': 'Events',
                'eras': era_infos,
                'dbcache': 'dascache',
                'samples': sample_infos,
                'plotIt': self.plot_info(year),
            }
            config_file_name = os.path.join(self.config_path,f'config_{self.get_unique_name(year)}.yml')
            with open(config_file_name, 'w') as f:
                yaml.dump(info,f, indent=2, sort_keys=False) 

    def RunAnalyser(self, distributed, maxFiles):
        ''' Options for distributed: [sequential, parallel, driver]'''
        module_name = self.module_name.replace(self.local_path+'/','')
        for year in self.years:
            print(green(f'--> Runnnig bambooRun for {year}'))
            config_file_name = os.path.join(self.config_path,f'config_{self.get_unique_name(year)}.yml').replace(self.local_path+'/','')
            outpath = os.path.join(self.output_path,self.get_unique_name(year)).replace(self.local_path+'/','')
            cmd = f'bambooRun -m {module_name} {config_file_name} -o {outpath} --distributed {distributed} --envConfig bamboo.init'
            if maxFiles:
                cmd += f' --maxFiles {maxFiles}'
            print(green('  --> Executing command: '+cmd))
            subprocess.run(cmd, shell=True)
            print(green(f'--> Finished running for {year}'))

    def Submit(self, maxFiles=None):
        self.RunAnalyser(distributed='driver', maxFiles=maxFiles)
    
    def RunLocal(self,distributed='sequential', maxFiles=None):
        self.RunAnalyser(distributed=distributed, maxFiles=maxFiles)

    def Test(self, distributed='sequential', maxFiles=1):
        self.RunLocal(distributed=distributed, maxFiles=maxFiles)

    