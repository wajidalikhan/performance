import os, sys, itertools
from collections import OrderedDict
from printing_utils import green, blue, prettydict

from Constants import Constants

class GenericPath:
    ''' Class container for paths '''
    def __init__(self):
        self.username = os.environ['USER']
        self.jme_path = os.environ['JMEVALIDATIONPATH']
        self.config_path = os.path.join(self.jme_path, 'config')


class VariablesBase(GenericPath):
    ''' Class container for list of objects '''
    def __init__(self):
        GenericPath.__init__(self)
        self.RunPeriods_Dict    = {'2022': ['C', 'D', 'E', 'F', 'G'],
                                   }
        self.Datasets           = ['DY', 'Muon']
        self.years              = sorted(self.RunPeriods_Dict.keys())
        self.AllRunPeriods      = list(set(itertools.chain.from_iterable(self.RunPeriods_Dict.values())))
        self.defineGroups()
    
    def defineGroups(self):
        self.groups = OrderedDict()
        self.groups.setdefault('TTbar',['TTbar'])

            
class ModuleRunner(VariablesBase, Constants):
    ''' Class container for list of objects for particular year '''
    def __init__(self, years, ModuleName):
        VariablesBase.__init__(self)
        Constants.__init__(self)
        self.years = years
        self.ModuleName = ModuleName+'Module.py'
        self.ncores = 3
        # self.lumi_fb  = round(float(ROOT.Year2Lumi[self.year]),1)
        print(self)

    def __str__(self):
        print(blue('--> ModuleRunner info:'))
        prettydict(self.__dict__)
        return blue('--> ModuleRunner info: end.')

    def CreateConfigFiles(self):
        import yaml
        for year in self.years:
            era_infos = {year: {'luminosity': self.lumi[year]}}
            sample_infos = {}
            for ds in self.Datasets:
                sample_infos[ds] = {
                    'era': year,
                    'group': ds,
                    # 'db': 'das:/TTTo2L2Nu_CP5_13p6TeV_powheg-pythia8/Run3Winter22NanoAOD-122X_mcRun3_2021_realistic_v9-v1/NANOAODSIM',
                    'files': self.files[ds],
                    'type': self.type[ds],
                    'split': 34,
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
            config_file_name = os.path.join(self.config_path,f'config_{year}.yml')
            with open(config_file_name, 'w') as f:
                yaml.dump(info,f, indent=2, sort_keys=False) 

    # def RunAnalyser(self, options):
    #     commands = []
    #     path = os.path.join(self.config_path, 'workdir_'+self.ModuleName)
    #     for year in self.years:
    #         xmlfilename = os.path.join(self.config_path, 'workdir_'+self.ModuleName, self.ModuleName+'Config_'+year+'.xml')
    #         commands.append([path, 'submit.py %s -%s' %(xmlfilename, options)])
    #     a = parallelize(commands, ncores=self.ncores, cwd=True, remove_temp_files=False)

    # def CleanWorkdirs(self):
    #     self.RunAnalyser(options='c')

    # def Split(self):
    #     self.RunAnalyser(options='d')

    # def Submit(self):
    #     self.CompileCode()
    #     self.RunAnalyser(options='s')

    # def Resubmit(self):
    #     self.RunAnalyser(options='s')

    # def CheckStatus(self):
    #     self.RunAnalyser(options='o')

    # def Merge(self):
    #     self.RunAnalyser(options='f')
    #     # self.RunAnalyser(options='p')

    # def RunLocal(self,ncores=4):
    #     import glob, sys
    #     if not ncores:
    #         ncores = self.ncores
    #     print(green('--> Locally running jobs on %i cores' % (ncores)))
    #     commands = []
    #     path = os.path.join(self.config_path, 'workdir_'+self.ModuleName)
    #     for year in self.years:
    #         for missing_files in glob.glob(os.path.join(self.config_path, 'workdir_'+self.ModuleName, 'workdir_'+self.ModuleName+'Config_'+year,'*','commands_missing_files.txt')):
    #             with open(missing_files, 'r') as f:
    #                 for l in f.readlines():
    #                     commands.append(l.rstrip('\n'))
    #     commands = [[self.config_path, c] for c in commands]
    #     parallelize(commands, ncores=ncores, cwd=True)
    #     print(green('--> Finished running missing jobs locally.'))

    