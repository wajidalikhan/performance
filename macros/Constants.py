class Constants():
    def __init__(self):
        self.lumi = {
            '2022': 4960,
        }
        self.lumi_legend = {
            '2022': '34',
        }
        self.year_legend = {
            '2022': '2022',
        }
        self.energy = {
            '2022': '13.6',
        }
        self.pileup = {
            '2022': 43,
        }
        self.xsec = {
            'TTbar': 831.76,
            'DY':    5558,
        }
        self.type = {
            'TTbar': 'mc',
            'DY':    'mc',
            'Muon':  'data',
        }
        self.files = {
            'TTbar': 'datasets/TTbar_2022_Winter22_Nano10_das.txt',
            'DY':    'datasets/DY_2022_Winter22_Nano10_jme.txt',
            'Muon':  'datasets/Muon_2022RunC_Prompt_Nano10_jme.txt',
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
                'TTbar': {'legend': 'TTbar', 'fill-color': "#99ccff",},
                'DY':    {'legend': 'DY',    'fill-color': "#9FFF33",},
                'WJets': {'legend': 'WJets', 'fill-color': "#FFC300",},
                'VV':    {'legend': 'VV',    'fill-color': "#C900FF",},
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

