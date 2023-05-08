class Constants():
    def __init__(self):
        self.lumi = {
            '2022': {'C': 4.96,'D': 2.94,'E': 5.84,'F': 17.80, 'G': 2},
        }
        self.energy = {
            '2022': '13.6',
        }
        self.pileup = {
            '2022': 43,
        }
        self.year_run_map = {
            '2022': ['C','D','E','F','G'],
        }
        self.MC_samples = ['DY','TTbar','QCD_Flat']
        self.data_samples = ['Muon', 'JetHT']
        self.modules = {
            'DY':    ['Muon',  'DY'],
            'TTbar': ['Muon',  'TTbar'],
            'QCD':   ['JetHT', 'QCD_Flat'],
        }
        self.xsec = {
            'TTbar':  831.76,
            'DY':     5558,
            'QCD_Flat':   185900000*10, #from QCD_HT100to200 * 10
        }
        self.files = {
            '2022': {
                'Winter22': {
                    'DY':       'datasets/DY_2022_Winter22_Nano10_jme.txt',
                    'QCD_Flat': 'datasets/QCD_Pt_15to7000_Flat_2022_Winter22_Nano10_jme.txt',
                },
                'Summer22': {
                    # 'DY':       'datasets/DY_2022_Summer22_Nano10_jme.txt',
                    'QCD_Flat': 'datasets/QCD_Pt_15to7000_Flat_2022_Summer22_Nano11_das.txt',
                },
                'Summer22EE': {
                    # 'DY':       'datasets/DY_2022_Summer22EE_Nano10_jme.txt',
                    'QCD_Flat': 'datasets/QCD_Pt_15to7000_Flat_2022_Summer22EE_Nano11_das.txt',
                },
                'Prompt':{
                    'MuonC':    'datasets/Muon_2022RunC_Prompt_Nano10_jme.txt',
                    'MuonD':    'datasets/Muon_2022RunD_Prompt_Nano10_jme.txt',
                    'MuonE':    'datasets/Muon_2022RunE_Prompt_Nano10_jme.txt',
                    'MuonF':    'datasets/Muon_2022RunF_Prompt_Nano10_jme.txt',
                    'MuonG':    'datasets/Muon_2022RunG_Prompt_Nano10_das.txt',
                },
                'ReReco':{
                    'MuonC':    'datasets/Muon_2022RunC_ReReco_Nano11_das.txt',
                    'MuonD':    'datasets/Muon_2022RunD_ReReco_Nano11_das.txt',
                    'MuonE':    'datasets/Muon_2022RunE_ReReco_Nano11_das.txt',
                }
            },
            '2023': {
                'Winter23': {
                    # 'QCD_Flat': 'datasets/QCD_Pt_15to7000_Flat_2022_Winter23_Nano10_jme.txt',
                    # 'QCD_Flat_Fix': 'datasets/QCD_Pt_15to7000_Flat_2022_Winter23_Nano10_jme.txt',
                },
            }
        }

        self._plot_info = {
            'configuration': {
                'width': 800,
                'height': 600,
                'margin-left': 0.2,
                'margin-right': 0.03,
                'margin-top': 0.05,
                'margin-bottom': 0.15,
                'luminosity-label': 'None',
                'experiment': 'CMS',
                'extra-label': 'Work in progress',
                'error-fill-style': 3154,
                'error-fill-color': "#ee556270",
                'ratio-fit-error-fill-style': 1001,
                'ratio-fit-error-fill-color': "#aa556270",
                'ratio-fit-line-color': "#0B486B",
                'yields-table-align': 'v',
            },
            'legend': {'position': [0.7, 0.6, 0.91, 0.91]},
            'groups': {
                'data':  {'legend': 'data'},
                'DY':    {'legend': 'DY',    'fill-color': "#609e1b",},
                'TTbar': {'legend': 'TTbar', 'fill-color': "#99ccff",},
                'QCD':   {'legend': 'QCD',   'fill-color': "#FFC300",},
                'WJets': {'legend': 'WJets', 'fill-color': "#9c04c4",},
            },
            'plotdefaults': {
                'y-axis': 'Events',
                'log-y': 'both',
                'y-axis-show-zero': True,
                'save-extensions': ['pdf'],
                'show-ratio': True,
                'sort-by-yields': True,
                'legend-columns': 2,
                'ratio-y-axis': '#frac{Data}{MC}',
                'ratio-y-axis-range': [0.8, 1.2],
                'normalized': False,
            },
        }
    
    def plot_info(self, year, cms_label='Work in progress'):
        new_dict = self._plot_info.copy()
        new_dict['configuration']['luminosity-label'] = f'{year}, %1$.2f fb^{-1} ({self.energy[year]} TeV)'
        new_dict['configuration']['extra-label'] = cms_label
        return new_dict
    
    def get_datasets(self, year, runs):
        return self.MC_samples + [d+r for d in self.data_samples for r in self.year_run_map[year] if r in runs]
    
    def get_lumi(self,year,runs):
        tot_lumi = 0
        for run, lumi in self.lumi[year].items():
            if run in runs:
                tot_lumi += lumi*1000
        return int(tot_lumi)
    
    def get_type(self, year, dataset):
        if dataset in self.MC_samples: return 'mc'
        if dataset in [d+r for d in self.data_samples for r in self.year_run_map[year]]: return 'data'
        raise ValueError(f'{dataset} is neither mc nor data')
    
    def get_files(self, year, campaigns, dataset):
        type_ = self.get_type(dataset=dataset,year=year)
        campaign = campaigns[type_]
        return self.files[year][campaign][dataset]