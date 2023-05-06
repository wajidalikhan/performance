from bamboo import treefunctions as op
from bamboo.plots import Plot
from bamboo.plots import EquidistantBinning as EqBin

def muonPlots(muons, sel, sel_tag, maxMuons = 4):
    plots = []

    plots.append(Plot.make1D(f"{sel_tag}_Muon_nMuons", op.rng_len(muons), sel, EqBin(15, 0., 15.),xTitle = "Number of muons"))
    
    #### do a for loop through all Muons
    for i in range(maxMuons):
        plots.append(Plot.make1D(f"{sel_tag}_Muon{i+1}_pt", muons[i].pt, sel, EqBin(20, 0., 500.), xTitle=f"muon_{{{i+1}}} p_{{T}} [GeV]"))
        plots.append(Plot.make1D(f"{sel_tag}_Muon{i+1}_eta", muons[i].eta, sel, EqBin(20, -2.5, 2.5), xTitle=f"muon_{{{i+1}}} #eta"))
        plots.append(Plot.make1D(f"{sel_tag}_Muon{i+1}_phi", muons[i].phi, sel, EqBin(20, -2.5, 2.5), xTitle=f"muon_{{{i+1}}} #phi"))
 
    return plots


def electronPlots(electrons, sel, sel_tag, maxElectrons = 4):
    plots = []

    plots.append(Plot.make1D(f"{sel_tag}_Electron_nElectrons", op.rng_len(electrons), sel, EqBin(15, 0., 15.), xTitle=f"Number of Electrons"))
    
    #### do a for loop through all Electrons
    for i in range(maxElectrons):
        plots.append(Plot.make1D(f"{sel_tag}_Electron{i+1}_pt", electrons[i].pt, sel, EqBin(20, 0., 500.), xTitle=f"electron_{{{i+1}}} p_{{T}} [GeV]"))
        plots.append(Plot.make1D(f"{sel_tag}_Electron{i+1}_eta", electrons[i].eta, sel, EqBin(20, -2.5, 2.5), xTitle=f"electron_{{{i+1}}} #eta"))
        plots.append(Plot.make1D(f"{sel_tag}_Electron{i+1}_phi", electrons[i].phi, sel, EqBin(20, -2.5, 2.5), xTitle=f"electron_{{{i+1}}} #phi"))
 
    return plots


def AK4jetPlots(jets, sel, sel_tag, maxJets=4):
    plots = []

    plots.append(Plot.make1D(f"{sel_tag}_AK4Jets_nJets",op.rng_len(jets),sel,EqBin(15,0.,15.), xTitle=f"Number of Jets"))
    #### do a for loop through all Jets
    for i in range(maxJets):
        plots.append(Plot.make1D(f"{sel_tag}_Jet{i+1}_pt", jets[i].pt, sel, EqBin(20, 0., 500.), xTitle=f"jet_{{{i+1}}} p_{{T}} [GeV]"))
        plots.append(Plot.make1D(f"{sel_tag}_Jet{i+1}_eta", jets[i].eta, sel, EqBin(20, -2.5, 2.5), xTitle=f"jet_{{{i+1}}} #eta"))
        plots.append(Plot.make1D(f"{sel_tag}_Jet{i+1}_phi", jets[i].phi, sel, EqBin(20, -2.5, 2.5), xTitle=f"jet_{{{i+1}}} #phi"))

    return plots



def ZbosonPlots(Zboson, sel, sel_tag):
    plots = []

    plots.append(Plot.make1D(f"{sel_tag}_Zboson_mass",Zboson.M(),sel,EqBin(30,0.,200.),xTitle="m_{ll} [GeV]"))

    plots.append(Plot.make1D(f"{sel_tag}_Zboson_pt",Zboson.pt,sel,EqBin(30,0.,200.),xTitle="Z boson p_{T} [GeV]"))
