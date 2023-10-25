#! /usr/bin/env python

import os
from math import sqrt
from collections import OrderedDict
from tdrstyle_JME import *
import tdrstyle_JME as TDR
rt.gROOT.SetBatch(rt.kTRUE)
rt.gStyle.SetOptStat(0)
rt.gStyle.SetOptFit(0)


def ominus(a,b):
    return sqrt(max(a*a-b*b,0.0))

def oplus(a,b):
    return sqrt(a*a+b*b)

def getMedianError(hist):
    if hist.GetEffectiveEntries()!=0:
        return 1.253 * hist.GetRMS() / sqrt(hist.GetEffectiveEntries())
    else: return 0

def MakeRatioHistograms(h1, h2, name):
    hratio = h1.Clone(name)
    for bin in range(1,h1.GetNbinsX()+1):
        r, dr = (0,0)
        num = h1.GetBinContent(bin)
        den = h2.GetBinContent(bin) 
        if den!=0 and num!=0:
            r = num/den
            dr = r*oplus(h1.GetBinError(bin)/num,h2.GetBinError(bin)/den)
        hratio.SetBinContent(bin, r)
        hratio.SetBinError(bin, dr)
    return hratio

def Confidence(h1, median, confLevel = 0.95):
    ix = h1.GetXaxis().FindBin(median)
    ixlow = ix
    ixhigh = ix
    nb = h1.GetNbinsX()
    ntot = h1.Integral()
    nsum = h1.GetBinContent(ix)
    width = h1.GetBinWidth(ix)
    if ntot==0: return 0
    while (nsum < confLevel * ntot):
        nlow = h1.GetBinContent(ixlow-1) if ixlow>0 else 0
        nhigh = h1.GetBinContent(ixhigh+1) if ixhigh<nb else 0
        if (nsum+max(nlow,nhigh) < confLevel * ntot):
            if (nlow>=nhigh and ixlow>0):
                nsum += nlow
                ixlow -=1
                width += h1.GetBinWidth(ixlow)
            elif ixhigh<nb:
                nsum += nhigh
                ixhigh+=1
                width += h1.GetBinWidth(ixhigh)
            else: raise ValueError('BOOM')
        else:
            if (nlow>nhigh):
                width += h1.GetBinWidth(ixlow-1) * (confLevel * ntot - nsum) / nlow
            else:
                width += h1.GetBinWidth(ixhigh+1) * (confLevel * ntot - nsum) / nhigh
            nsum = ntot
    return width


class MakePlots():
    def __init__(self, year, path, fname, pdfextraname=''):
        self.eta_bins = ['0p0to5p2', '0p0to1p3','1p3to2p4','2p4to2p7','2p7to3p0','3p0to5p2']
        # self.eta_bins = ['0p0to1p3']
        self.pt_bins = ['15to17','17to20','20to23','23to27','27to30','30to35','35to40','40to45','45to57','57to72','72to90','90to120','120to150','150to200','200to300','300to400','400to550','550to750','750to1000','1000to1500','1500to2000','2000to2500','2500to3000','3000to3500','3500to4000','4000to4500','4500to5000']
        # self.pt_bins = ['150to200']

        self.types = {
            'effPurity': [('allrecojets',  ['reco','gen','unmatchedgen','unmatchedreco' ]), ('puritymatched', ['reco']), ('effmatched', ['gen'])]
        }
        self.response_names = ['dijet','noLepton','noSel','Zmasscut']
        
        self.year = year
        self.fname = fname
        self.inputPath = path
        self.outputPath = os.path.join(self.inputPath,'pdfs')
        for fold in self.types.keys():
            os.system('mkdir -p '+os.path.join(self.outputPath,fold))
        self.pdfextraname = pdfextraname

    
    def LoadInputs(self):
        self.files = OrderedDict()
        self.hists = OrderedDict()
        self.graphs = OrderedDict()
        self.files[self.fname] = rt.TFile(os.path.join(self.inputPath,f'{self.fname}.root'))
        f_ = self.files[self.fname]
        # remove response names, that do not exist
        lista = [ el.GetName().split("_")[0] for el in f_.GetListOfKeys() if "response" in el.GetName()]
        self.response_names = [el for el in self.response_names if el in lista]

        self.quant   = array('d',[0.5])
        self.quant_y   = array('d',[0.5])
        for eta_bin in self.eta_bins:
            for response_name in self.response_names:
                pts, jes, jer, pts_err, jes_err, jer_err = ([],[],[],[],[], [])
                for pt in self.pt_bins:
                    hname = f'{response_name}_response_eta{eta_bin}_pt{pt}'
                    # hname = f'response_eta{eta_bin}_pt{pt}'
                    hist = f_.Get(hname)
                    hist.GetQuantiles(1,self.quant_y,self.quant)
                    pt_min, pt_max = pt.split('to')
                    pt_min, pt_max = int(pt_min), int(pt_max)
                    pts.append((pt_max+pt_min)/2)
                    pts_err.append((pt_max-pt_min)/2)
                    jes.append(self.quant_y[0])
                    jer.append(Confidence(hist, hist.GetMean(), confLevel = 0.87)/(2*1.514))
                    jes_err.append(getMedianError(hist))
                    jer_err.append(hist.GetRMSError())
                self.graphs[response_name+eta_bin+'jes'] = rt.TGraphErrors(len(pts), array('d',pts), array('d',jes), array('d',pts_err), array('d',jes_err))
                self.graphs[response_name+eta_bin+'jer'] = rt.TGraphErrors(len(pts), array('d',pts), array('d',jer), array('d',pts_err), array('d',jer_err))
            
            for mode, types in self.types.items():
                for type, jets in types:
                    for jet in jets:
                        hname = f'{mode}_{type}_eta{eta_bin}_{jet}pt'
                        self.hists[hname] = f_.Get(hname)
                        self.hists[hname].SetDirectory(0)
                        if type != 'allrecojets':
                            hname_new = f'{mode}_{type}_eta{eta_bin}'
                            self.hists[hname_new] = self.hists[hname].Clone(hname_new)
                            # print("Dividing", hname, 'by', hname.replace(type,'allrecojets').replace(jet+'pt','unmatchedgenpt'), 'into', hname_new )
                            num = self.hists[hname]
                            if 'eff' in type:
                                den = self.hists[hname.replace(type,'allrecojets').replace(jet+'pt','unmatchedgenpt')]
                            if 'purity' in type:
                                den = self.hists[hname.replace(type,'allrecojets').replace(jet+'pt','unmatchedrecopt')]
                            self.hists[hname_new].Divide(num, den, 1, 1, 'B')
                            # self.hists[hname_new] = MakeRatioHistograms(self.hists[hname], self.hists[hname.replace(type,'allrecojets')], hname_new)
                            self.hists[hname_new].SetDirectory(0)
    
                
    def Close(self):
        self.files['save'] = rt.TFile(os.path.join(self.outputPath, 'resp_eff_pur_plots.root'), 'Recreate')
        for name, graph in self.graphs.items():
            graph.Write(name)
        for name, hist in self.hists.items():
            hist.Write(name)
        for f_ in self.files.values():
            f_.Close()

    def CreateCanvas(self, canvName='', zoom=True, nEntries=7):
        if 'canv' in self.__dict__: self.canv.Close()
        XMin, XMax = (15, 7500)
        YMin, YMax = (0.9,1.1) if zoom else (0.0,2)
        if 'response' in canvName.lower(): xName, yName = ('Gen jet p_{T} [GeV]', 'Response')
        elif 'effmatched' in canvName.lower(): xName, yName = ('Gen jet p_{T} [GeV]', 'Efficiency')
        elif 'puritymatched' in canvName.lower(): xName, yName = ('Reco jet p_{T} [GeV]', 'Purity')
        else: xName, yName = ('', '')
        TDR.extraText   = 'Simulation'
        TDR.extraText2  = 'Preliminary'
        TDR.cms_lumi = TDR.commonScheme['legend'][self.year]
        TDR.cms_energy = TDR.commonScheme['energy'][self.year]
        TDR.extraText3 = []
        TDR.extraText3.append('AK4 Puppi')
        self.canv = tdrCanvas(canvName, XMin, XMax, YMin, YMax, xName, yName, square=kSquare, isExtraSpace=True)
        self.canv.SetLogx(True)
        self.leg  = tdrLeg(0.60,0.90-(nEntries+1)*0.040,0.90,0.90)
        FixXAsisPartition(self.canv)
        self.lines= {}
        for y in [0]:
            self.lines[y] = rt.TLine(XMin, y, XMax, y)
            tdrDrawLine(self.lines[y], lcolor=rt.kBlack, lstyle=rt.kDashed, lwidth=1)
    
   
    def PlotResponse(self, response_name ='response'):
        infos = {
            '0p0to1p3' : {'legend': '0.0 < |#eta| < 1.3', 'color':  rt.kGreen+3,  'marker': rt.kFullSquare,       'msize':  1.0},
            '1p3to2p4' : {'legend': '1.3 < |#eta| < 2.4', 'color':  rt.kBlue-4,   'marker': rt.kFullStar,         'msize':  1.3},
            '2p4to2p7' : {'legend': '2.4 < |#eta| < 2.7', 'color':  rt.kAzure+2,  'marker': rt.kFullCrossX,       'msize':  1.3},
            '2p7to3p0' : {'legend': '2.7 < |#eta| < 3.0', 'color':  rt.kRed+1,    'marker': rt.kFullTriangleUp,   'msize':  1.0},
            '3p0to5p2' : {'legend': '3.0 < |#eta| < 5.2', 'color':  rt.kOrange+1, 'marker': rt.kFullTriangleDown, 'msize':  1.0},
            '0p0to5p2' : {'legend': '0.0 < |#eta| < 5.2', 'color':  rt.kBlack,    'marker': rt.kFullCircle,       'msize':  1.0},
        }

        self.CreateCanvas(canvName='response_'+response_name, zoom=True)
        for name, graph in self.graphs.items():
            if not 'jes' in name: continue
            if not response_name in name: continue
            info = infos[name.replace('jes','').replace(response_name,'')]
            tdrDraw(graph, 'P', msize=info['msize'], marker=info['marker'], mcolor=info['color'])
            self.leg.AddEntry(graph, info['legend'], 'lp')
        self.canv.SaveAs(os.path.join(self.outputPath, 'response_'+response_name + self.pdfextraname + '.pdf'))

    def PlotEffPurity(self):
        for eta_bin in self.eta_bins:
            for mode, types in self.types.items():
                if mode != 'effPurity': continue
                for type, _ in types:
                    if type == 'allrecojets': continue
                    isEff = 'effmatched' in type
                    hname = f'{mode}_{type}_eta{eta_bin}'
                    self.CreateCanvas(canvName=hname, zoom=False)
                    hist = self.hists[hname]
                    tdrDraw(hist, 'P', fstyle=0)
                    # tdrDraw(h, opt, marker=rt.kFullCircle, msize=1.0, mcolor=rt.kBlack, lstyle=rt.kSolid, lcolor=-1, fstyle=1001, fcolor=rt.kYellow+1, alpha=-1):
                    self.canv.SaveAs(os.path.join(self.outputPath, mode,  hname + self.pdfextraname + '.pdf'))

        # #     legname, color = self.info[type]
        # #     if pdfname!=shape: legname, color = self.info[shape]
        # #     if extraName!=None and not (extraName in type or extraNamejobs in shape): continue
        # #     if pdfname in type or pdfname in shape:
        # #         tdrDraw(hist, 'P', mcolor=color)
        # #         list(hist.GetListOfFunctions())[0].SetLineColor(color)
        # #         self.leg.AddEntry(hist, legname, 'pl')
        # if extraName!=None: pdfname += extraName
    
    def PlotAll(self):
        self.LoadInputs()
        for response_name in self.response_names:
            self.PlotResponse(response_name=response_name)
        self.PlotEffPurity()
        self.Close()




def main():
    MP = MakePlots().PlotAll()

if __name__ == '__main__':
    main()
