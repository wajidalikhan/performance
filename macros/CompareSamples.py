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
            outputPath = GenericPath().jme_path
        self.outputPath = os.path.join(outputPath,'pdfs/CompareSamples')
        os.system('mkdir -p '+os.path.join(self.outputPath))
        self.pdfextraname = pdfextraname
        TDR.extraText   = 'Simulation'
        TDR.extraText2  = 'Preliminary'
        TDR.cms_lumi = TDR.commonScheme['legend'][self.year]
        TDR.cms_energy = TDR.commonScheme['energy'][self.year]
        self.infos = {
            'color': [rt.kBlack, rt.kGreen+2, rt.kRed+1, rt.kOrange+1]
        }
        

    
    def LoadInputs(self):
        self.files = OrderedDict()
        self.hists = OrderedDict()
        for sname, fname in self.samples.items():
            print (fname)
            self.files[sname] = rt.TFile(fname)
            print(self.files[sname])
            for hname in self.histsname:
                h = self.files[sname].Get(hname)
                h.SetDirectory(0)
                h.Rebin(2)
                h.Scale(1./h.Integral())
                self.hists[sname+hname] = h
    
                
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
            tdrDraw(h, 'P', mcolor=self.infos['color'][s_ind], fstyle=0)
            self.leg.AddEntry(h, sname.replace('NPV','').replace('A','A = ').replace('B','; B = ').replace('p','.'), 'lp')
            self.canv.cd(2)
            self.hists[sname+histname+'ratio'] = h.Clone(sname+histname+'ratio')
            self.hists[sname+histname+'ratio'].Divide(h_ref_ratio)
            tdrDraw(self.hists[sname+histname+'ratio'], 'P', mcolor=self.infos['color'][s_ind], fstyle=0)
        self.canv.SaveAs(os.path.join(self.outputPath, f'{histname}{self.pdfextraname}.pdf'))
        self.canv.Close()

  
    def PlotAll(self):
        self.LoadInputs()
        for hname in self.histsname:
            self.Plot(histname=hname)
        self.Close()




def main():

    histsname = ['ZmasscutJetID_Jet1_eta']

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
