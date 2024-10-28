class Constants():
    def __init__(self):
        self.lumi = {
            '2022': {'C': 4.96,'D': 2.94,'E': 5.84,'F': 17.80, 'G': 2},
            'UL18': {'A': 4.96,'B': 2.94,'C': 5.84,'D': 17.80},
        }
        self.energy = {
            '2022': '13.6',
            'UL18': '13.6',
        }
        self.pileup = {
            '2022': 43,
            'UL18': 32,
        }
        self.year_run_map = {
            '2022': ['C','D','E','F','G'],
            'UL18': ['A','B','C','D'],
        }
        
        #self.MC_samples = ['DY','TTbar','QCD_Flat', 'DYTau']
        #self.MC_samples = ['DY','TTbar','QCD_Flat']
        #self.MC_samples = ['DY']
        
        self.MC_samples = ['DY','TTbar','QCD_Flat','WJets']
        self.data_samples = ['Muon']
        self.modules = {
            #'DY':    ['Muon'],
            #'DY':    ['DY'],
            #'DY':    ['DY', 'Muon'],
            'DY':    ['DY', 'TTbar', 'QCD_Flat','WJets', 'Muon'],

            'TTbar': ['Muon',  'TTbar'],
            'QCD':   ['JetHT', 'QCD_Flat'],
            'test':   ['JetHT', 'QCD_Flat'],
            'NanoJME':   ['JetHT', 'QCD_Flat'],
        }
        self.xsec = {
            'WJets':        64481.5,
            'TTbar':        831.76,
            'DY':           5558,
            'DYTau':        5558,
            'QCD_Flat':     185900000, #from QCD_HT100to200 * 10
        }
        self.files = {
            'UL18':{
                'Summer20UL':{
                    'QCD_Flat' : 'datasets/QCD_Pt_15to7000_Flat_2018_Summer20_JMENano.txt',
                },
            },
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
                'Summer22EETau4GeV': {
                    # 'DY':       'datasets/DY_2022_Summer22EE_Nano10_jme.txt',
                    'QCD_Flat': 'datasets/QCD_Pt_15to7000_Flat_2022_Summer22EE_Tau4GeV.txt',
                },
                'Summer22EETau10GeV': {
                    # 'DY':       'datasets/DY_2022_Summer22EE_Nano10_jme.txt',
                    'QCD_Flat': 'datasets/QCD_Pt_15to7000_Flat_2022_Summer22EE_Tau10GeV.txt',
                },
                'Summer22EEFromPV2Tau4GeV': {
                    'DY':       'datasets/DY_Summer23_fromPV4GeV_v2.txt',
                    'QCD_Flat': 'datasets/QCD_Summer23_fromPV4GeV_v2.txt',
                    'DYTau': 'datasets/DYto2TautoMuTauh_Summer23_fromPV4GeV_v2.txt',
                    'TTbar': 'datasets/TTbar_Summer23_fromPV4GeV_v2.txt',
                },
                'Summer22EEFromPV2Tau0GeV': {
                    # 'DY':       'datasets/DY_Summer23_fromPV0GeV_v2.txt',
                    # 'QCD_Flat': 'datasets/QCD_Summer23_fromPV4GeV_v2.txt',
                    'DYTau': 'datasets/DYto2TautoMuTauh_Summer23_fromPV0GeV_v2.txt',
                    # 'TTbar': 'datasets/TTbar_Summer23_fromPV4GeV_v2.txt',
                },
                'Summer22EEnoCandRemoval': {
                    # 'DY':       'datasets/DY_2022_Summer22EE_Nano10_jme.txt',
                    'QCD_Flat': 'datasets/QCD_Pt_15to7000_Flat_2022_Summer22EE_noCandRemoval.txt',
                },
                'Summer22EENOMINAL': {
                    'DY':       'datasets/DY_Summer23_NOMINAL.txt',
                    'QCD_Flat': 'datasets/QCD_Summer23_NOMINAL.txt',
                    'TTbar':    'datasets/TTbar_Summer23_NOMINAL.txt',
                    'WJets':    'datasets/WJets_Summer23_NOMINAL.txt',
                },
                'Prompt':{
                    'MuonC':    'datasets/Muon_Run2022C_Prompt_16Dec2023.txt',
                    'MuonD':    'datasets/Muon_Run2022D_Prompt_16Dec2023.txt',
                    'MuonE':    'datasets/Muon_Run2022E_Prompt_16Dec2023.txt',
                    'MuonF':    'datasets/Muon_Run2022F_Prompt_16Dec2023.txt',
                    'MuonG':    'datasets/Muon_Run2022G_Prompt_16Dec2023.txt',
                },
                'ReReco':{
                    'MuonC':    'datasets/Muon_2022RunC_ReReco_Nano11_das.txt',
                    'MuonD':    'datasets/Muon_2022RunD_ReReco_Nano11_das.txt',
                    'MuonE':    'datasets/Muon_2022RunE_ReReco_Nano11_das.txt',
                    'JetHTC':   'datasets/JetHT_2022RunC_ReReco_Nano11_das.txt',
                    'JetHTD':   'datasets/JetHT_2022RunD_ReReco_Nano11_das.txt',
                    'JetHTE':   'datasets/JetHT_2022RunE_ReReco_Nano11_das.txt',
                },
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
                'data':     {'legend': 'data'},
                'DY':       {'legend': 'DY',    'fill-color': "#609e1b",},
                'TTbar':    {'legend': 'TTbar', 'fill-color': "#99ccff",},
                'QCD_Flat': {'legend': 'QCD',   'fill-color': "#FFC300",},
                'WJets':    {'legend': 'WJets', 'fill-color': "#9c04c4",},
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
                'normalized': True,
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
    
    def get_files(self, year, campaign, dataset):
        return self.files[year][campaign][dataset]
