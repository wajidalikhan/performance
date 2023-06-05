#! /usr/bin/env python
from utils import *


class CompareSamples():
    def __init__(self, samples, histsname, refsample=None, year='2022', outputPath = None, pdfextraname=''):
        self.samples = samples
        self.histsname = histsname
        self.refsample = refsample
        if self.refsample is None:
            self.refsample = list(self.samples.keys())[0]
        self.year = year
        if outputPath is None:
            from ModuleRunner import GenericPath
            outputPath = GenericPath().jme_path
        self.outputPath = os.path.join(outputPath,'pdfs/CompareSamples')
        os.system('mkdir -p '+os.path.join(self.outputPath))
        self.pdfextraname = pdfextraname
        TDR.extraText   = 'Simulation'
        TDR.extraText2  = 'Preliminary'
        TDR.cms_lumi = TDR.commonScheme['legend'][self.year]
        TDR.cms_energy = TDR.commonScheme['energy'][self.year]
        self.infos = {
            'color': {
                'Nominal':      rt.kBlack,
                'NPVA2p0B0p3':  rt.kOrange+1,
                'NPVA2p0B0p13': rt.kGreen+2,
                'NPVA3p0B0p13': rt.kRed+1,
                },
            'color_default': [rt.kBlack, rt.kGreen+2, rt.kRed+1, rt.kOrange+1]
        }
        self.eta_bins = ['0p0to5p2', '0p0to1p3','1p3to2p4','2p4to2p7','2p7to3p0','3p0to5p2']
    
    def LoadInputs(self):
        self.files = OrderedDict()
        self.hists = OrderedDict()
        for sname, fname in self.samples.items():
            self.files[sname] = rt.TFile(fname)
            for hname in self.histsname:
                h = self.files[sname].Get(hname)
                h.SetDirectory(0)
                h.Rebin(2)
                h.Scale(1./h.Integral())
                self.hists[sname+hname] = h
            if not any([x in self.pdfextraname for x in ['QCD', 'DY']]): continue
            fname = '/'.join(fname.split('/')[:-2]+['pdfs/resp_eff_pur_plots.root'])
            self.files[sname+'resp_eff_pur'] = rt.TFile(fname)
            for eta_bin in self.eta_bins:
                h = self.files[sname+'resp_eff_pur'].Get(f'effPurity_effmatched_eta{eta_bin}')
                h.SetDirectory(0)
                self.hists[sname+eta_bin] = h

    
                
    def Close(self):
        for f_ in self.files.values():
            f_.Close()
   
    def Plot(self, histname):
        h_ref = self.hists[self.refsample+histname]
        h_ref_ratio = self.hists[self.refsample+histname].Clone('h_ref_ratio')
        x_min = h_ref.GetBinLowEdge(1)
        y_max = h_ref.GetBinLowEdge(h_ref.GetNbinsX())
        self.canv = tdrDiCanvas(histname, x_min, y_max, 1e-04, 0.1, 0.4, 1.6, histname, 'A.U.', 'Ratio')
        # self.canv = tdrDiCanvas(histname, x_min, y_max, 1e-04, 1, 0.5, 1.5, histname, 'A.U.', 'Ratio')
        # self.canv.cd(1).SetLogy(True)
        self.leg  = tdrLeg(0.40,0.90-(len(self.samples)+1)*0.040,0.90,0.90)
        for s_ind, sname in enumerate(self.samples.keys()):
            h = self.hists[sname+histname]
            h.Scale(h_ref.Integral())
            self.canv.cd(1)
            color = self.infos['color'][sname] if sname in self.infos['color'] else self.infos['color_default'][s_ind]
            tdrDraw(h, 'P', mcolor=color, fstyle=0)
            self.leg.AddEntry(h, sname.replace('NPV','').replace('A','A = ').replace('B','; B = ').replace('p','.'), 'lp')
            self.canv.cd(2)
            self.hists[sname+histname+'ratio'] = h.Clone(sname+histname+'ratio')
            self.hists[sname+histname+'ratio'].Divide(h_ref_ratio)
            tdrDraw(self.hists[sname+histname+'ratio'], 'P', mcolor=color, fstyle=0)
        self.canv.SaveAs(os.path.join(self.outputPath, f'{histname}{self.pdfextraname}.pdf'))
        self.canv.Close()
    
    def PlotEff(self, eta_bin):
        if not any([x in self.pdfextraname for x in ['QCD', 'DY']]): return
        h_ref = self.hists[self.refsample+eta_bin]
        h_ref_ratio = self.hists[self.refsample+eta_bin].Clone('h_ref_ratio')
        eta_min, eta_max = eta_bin.replace('p','.').split('to')
        TDR.extraText3 = []
        TDR.extraText3.append(f'{eta_min} < |#eta| < {eta_max}')
        self.canv = tdrDiCanvas(eta_bin, 20, 3500, 0.5, 1.4, 0.5, 1.1, 'p_{T}^{gen}', 'A.U.', 'Ratio')
        # self.canv = tdrDiCanvas(eta_bin, x_min, y_max, 1e-04, 1, 0.5, 1.5, eta_bin, 'A.U.', 'Ratio')
        # self.canv.cd(1).SetLogy(True)
        self.canv.cd(1).SetLogx(True)
        self.canv.cd(2).SetLogx(True)
        FixXAsisPartition(self.canv.cd(2), shift=0.47, textsize=0.11, bins=[30,300,3000])
        self.canv.cd(1)
        self.leg  = tdrLeg(0.40,0.90-(len(self.samples)+1)*0.040,0.90,0.90)
        for s_ind, sname in enumerate(self.samples.keys()):
            h = self.hists[sname+eta_bin]
            self.canv.cd(1)
            color = self.infos['color'][sname] if sname in self.infos['color'] else self.infos['color_default'][s_ind]
            tdrDraw(h, 'P', mcolor=color, fstyle=0)
            self.leg.AddEntry(h, sname.replace('NPV','').replace('A','A = ').replace('B','; B = ').replace('p','.'), 'lp')
            self.canv.cd(2)
            self.hists[sname+eta_bin+'ratio'] = h.Clone(sname+eta_bin+'ratio')
            self.hists[sname+eta_bin+'ratio'].Divide(h_ref_ratio)
            tdrDraw(self.hists[sname+eta_bin+'ratio'], 'P', mcolor=color, fstyle=0)
        self.canv.SaveAs(os.path.join(self.outputPath, f'{eta_bin}{self.pdfextraname}.pdf'))
        self.canv.Close()

  
    def PlotAll(self):
        self.LoadInputs()
        for hname in self.histsname:
            self.Plot(histname=hname)
        for eta_bin in self.eta_bins:
            self.PlotEff(eta_bin=eta_bin)
        self.Close()




def main():
    selections = ['noSel', 'noSelJetID', 'noSelJetpt40', 'Zmasscut', 'ZmasscutJetID', 'ZmasscutJetpt40', 'ZmasscutJetpt100', 'ZmasscutJetetag2p4']
    types = ['AK4Jets_eta', 'Jet1_eta']
    histsname = [f'{sel}_{type}' for sel in selections for type in types]

    samples = {}
    samples['Nominal'] = 'outputs/DYModule/DY_2022_G_Winter22_Prompt_Summer22EERun3_V0_MC_Summer22EERun3_RunF_V0_DATA/results/MuonG.root'
    samples['NPVA2p0B0p13'] = 'outputs/DYModule/DY_2022_G_Summer22_NPVA2p0B0p13_PuppiTune_Summer22EERun3_V0_MC_Summer22EERun3_RunF_V0_DATA/results/MuonG.root'

    pdfextraname = '_Muon'
    MP = CompareSamples(samples=samples, histsname=histsname, pdfextraname=pdfextraname).PlotAll()

    samples = {}
    samples['Nominal'] = 'outputs/DYModule/DY_2022_G_Winter22_Prompt_Summer22EERun3_V0_MC_Summer22EERun3_RunF_V0_DATA/results/DY.root'
    samples['NPVA2p0B0p13'] = 'outputs/DYModule/DY_2022_G_Summer22_NPVA2p0B0p13_PuppiTune_Summer22EERun3_V0_MC_Summer22EERun3_RunF_V0_DATA/results/DY.root'
    

    pdfextraname = '_DY'
    MP = CompareSamples(samples=samples, histsname=histsname, pdfextraname=pdfextraname).PlotAll()

    histsname = ['DijetJetpt40_Jet1_eta']
    selections = ['Dijet','DijetJetID','DijetJetpt40','DijetJetpt100','DijetJetetas2p4','DijetJetetag2p4']
    types = ['AK4Jets_eta', 'Jet1_eta']
    histsname = [f'{sel}_{type}' for sel in selections for type in types]

    samples = {}
    samples['Nominal'] = 'outputs/QCDModule/QCD_2022_G_Summer22_Nominal_Prompt_Summer22EERun3_V0_MC_Summer22EERun3_RunF_V0_DATA/results/JetHTG.root'
    samples['NPVA2p0B0p13'] = 'outputs/QCDModule/QCD_2022_G_Summer22_NPVA2p0B0p13_PuppiTune_Summer22EERun3_V0_MC_Summer22EERun3_RunF_V0_DATA/results/JetHTG.root'

    pdfextraname = '_JetHT'
    MP = CompareSamples(samples=samples, histsname=histsname, pdfextraname=pdfextraname).PlotAll()
    
    samples = {}
    samples['Nominal'] = 'outputs/QCDModule/QCD_2022_G_Summer22_Nominal_Prompt_Summer22EERun3_V0_MC_Summer22EERun3_RunF_V0_DATA/results/QCD_Flat.root'

    # samples['RunD'] = 'outputs/QCDModule/QCD_2022_CD_Winter22_Prompt_Winter22Run3_V2_MC_Winter22Run3_RunD_V2_DATA/results/JetHTD.root'
    names = ['NPVA2p0B0p3', 'NPVA2p0B0p13', 'NPVA3p0B0p13']
    for name in names:
        samples[name] = f'outputs/QCDModule/QCD_2022_G_Summer22_{name}_PuppiTune_Summer22EERun3_V0_MC_Summer22EERun3_RunF_V0_DATA/results/QCD_Flat.root'
    
    pdfextraname = 'QCD'

    MP = CompareSamples(samples=samples, histsname=histsname, pdfextraname=pdfextraname).PlotAll()

if __name__ == '__main__':
    main()
