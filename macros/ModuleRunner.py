from utils import *

class GenericPath:
    ''' Class container for paths '''
    def __init__(self):
        self.username = os.environ['USER']
        self.jme_path = os.environ['JMEVALIDATIONPATH']
        self.local_path = os.environ['PWD']
        self.config_path = os.path.join(self.jme_path, 'config')
        self.module_path = os.path.join(self.jme_path, 'modules')
        os.system('mkdir -p '+self.config_path)
        os.system('mkdir -p '+self.module_path)


class ModuleRunner(GenericPath, Constants):
    ''' Class container for list of objects for particular year '''
    def __init__(self, module, years, runs, campaigns, jecs=None, extraName=None, extra_info={}):
        GenericPath.__init__(self)
        self.module = module
        self.module_name = os.path.join(self.module_path, self.module+'Module.py')
        self.output_path = os.path.join(self.jme_path,'outputs', self.module+'Module')
        self.years = years
        self.runs = runs
        self.campaigns = campaigns
        self.jecs = jecs
        self.extra_info = extra_info
        self._unique_name = f'{self.module}_year_{"".join(self.runs)}_{"_".join(self.campaigns.values())}_{"_".join(self.jecs.values())}'
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
            print(blue(f'--> Creating config for {year}'))
            era_infos = {year: {'luminosity': self.get_lumi(year,self.runs)}}
            sample_infos = {}
            for ds in self.get_datasets(year,self.runs):
                if not any([x in ds for x in self.modules[self.module]]): continue
                type_ = self.get_type(dataset=ds, year=year)
                if not type_ in self.campaigns: continue
                campaign = self.campaigns[type_]
                jec = self.jecs[type_] if self.jecs else ''
                sample_infos[ds] = {
                    'era': year,
                    'group': ds,
                    # 'db': 'das:/TTTo2L2Nu_CP5_13p6TeV_powheg-pythia8/Run3Winter22NanoAOD-122X_mcRun3_2021_realistic_v9-v1/NANOAODSIM',
                    'files': os.path.join(self.jme_path, self.get_files(year=year, campaign=campaign, dataset=ds)),
                    'type': type_,
                    'split': self.split_files_in,
                    'campaign': campaign,
                    'jec': jec,
                    }
                sample_infos[ds].update(self.extra_info)
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

    def RunAnalyser(self, distributed, maxFiles, **kargs):
        ''' Options for distributed: [sequential, parallel, driver]'''
        module_name = self.module_name.replace(self.local_path+'/','')
        for year in self.years:
            print(green(f'--> Runnnig bambooRun for {year}'))
            config_file_name = os.path.join(self.config_path,f'config_{self.get_unique_name(year)}.yml').replace(self.local_path+'/','')
            outpath = os.path.join(self.output_path,self.get_unique_name(year)).replace(self.local_path+'/','')
            cmd = f'bambooRun -m {module_name} {config_file_name} -o {outpath} --distributed {distributed} --envConfig bamboo.init'
            if maxFiles:
                cmd += f' --maxFiles {maxFiles}'
            if 'extra_flags' in kargs:
                cmd += ' '+kargs['extra_flags']
            print(green('  --> Executing command: '+cmd))
            subprocess.run(cmd, shell=True)
            print(green(f'--> Finished running for {year}'))

    def Submit(self, maxFiles=None, **kargs):
        print(blue('--> Running Submit'))
        self.RunAnalyser(distributed='driver', maxFiles=maxFiles, **kargs)
    
    def RunLocal(self,distributed='sequential', maxFiles=None, **kargs):
        print(blue('--> Running RunLocal'))
        self.RunAnalyser(distributed=distributed, maxFiles=maxFiles, **kargs)

    def Test(self, distributed='sequential', maxFiles=1, **kargs):
        print(blue('--> Running Test'))
        self.RunLocal(distributed=distributed, maxFiles=maxFiles)
        self.RunLocal(distributed=distributed, maxFiles=maxFiles, **kargs)
    
    def RunMissingLocal(self, ncores=10, remove_temp_files=True):
        from parallelize import parallelize
        print(blue('--> Running RunMissingLocal'))
        commands = []
        for year in self.years:
            outpath = os.path.join(self.output_path,self.get_unique_name(year)).replace(self.local_path+'/','')
            inputs = glob.glob(os.path.join(outpath, 'batch/input/condor_*.sh'))
            for input in inputs:
                output = input.replace('input/condor_','output/').replace('.sh','/')
                if len(glob.glob(output+'*root'))==0:
                    cmd = open(input).readlines()[-1]
                    cmd = cmd.replace(' && move_files','')
                    cmd = cmd.replace('--output=',f'--output={output}')
                    commands.append(cmd)
        if len(commands)!=0:
            parallelize(commands, ncores=ncores, remove_temp_files=remove_temp_files)
        else:
            print(blue('--> Nothing to run local'))
    
    def Merge(self, distributed='finalize', maxFiles=None, allow_incomplete=True, **kargs):
        if allow_incomplete:
            for year in self.years:
                outpath = os.path.join(self.output_path,self.get_unique_name(year)).replace(self.local_path+'/','')
                inputs = glob.glob(os.path.join(outpath, 'batch/output/*/*.root'))
                types = list(set([x.split('/')[-1] for x in inputs]))
                print(outpath, types)
                for type in types:
                    cmd = f'hadd -f {outpath}/results/{type} '
                    cmd += ' '.join(list(filter(lambda x: type in x, inputs)))
                    os.system(cmd)
            self.RunAnalyser(distributed='finalize', maxFiles=None, extra_flags='--onlypost', **kargs)
                
        else:
            self.RunAnalyser(distributed=distributed, maxFiles=maxFiles, **kargs)
    
    def Plot(self, pdfextraname=''):
        print(blue('--> Running Plot'))
        from MakePlots import MakePlots
        samples = list(filter(lambda x: x in self.MC_samples, self.modules[self.module]))
        for year in self.years:
            path = os.path.join(self.output_path,self.get_unique_name(year)).replace(self.local_path+'/','')
            for sample in samples:
                fname = os.path.join('results',sample)
                MP = MakePlots(year=year, path=path, fname=fname, pdfextraname=pdfextraname).PlotAll()

    