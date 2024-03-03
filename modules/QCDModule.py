
from bamboo.plots import Plot, CutFlowReport
from bamboo.plots import EquidistantBinning as EqBin
from bamboo import treefunctions as op
from bamboo.analysisutils import forceDefine

import src.definitions as defs

from modules.baseModule import NanoBaseJME


class QCDModule(NanoBaseJME):
    """"""

    def __init__(self, args):
        super(QCDModule, self).__init__(args)

    def definePlots(self, tree, noSel, sample=None, sampleCfg=None):
        plots = []
        yields = CutFlowReport("yields", printInLog=True, recursive=True)
        plots.append(yields)
        yields.add(noSel, 'No Selection')


        muons, electrons, clElectrons, ak4Jets, clak4Jets, ak4JetsID, ak4Jetspt40, ak4Jetspt100, ak4Jetsetas2p4, ak4Jetsetag2p4, ak8Jets, clak8Jets, clak4genjets = defs.defineObjects(tree)

        ### dijet selection
        noLepton = noSel.refine("noLepton", cut=(
            op.AND(
                op.rng_len(muons) == 0,
                op.rng_len(clElectrons) ==0
            )))


        dijet = noLepton.refine("dijet", cut = (
            op.AND(
                op.rng_len(clak4Jets)>1,
                # this introduces a bias in the JES and needs to be revised
                # clak4Jets[0].pt > 50,
                # op.deltaPhi(clak4Jets[0].p4,clak4Jets[1].p4)>2.7
            )))
        

        if sampleCfg['type'] == 'mc':
            pujets = defs.pujets(clak4Jets)
            matchedjets = defs.matchedjets(tree,clElectrons, muons, redo_match = True)

        #############################################################################
        #                                 Plots                                     #
        #############################################################################
        import src.controlPlots as cp

        if "all" in sampleCfg['plot_level']:
            ### noSel
            plots+=cp.muonPlots(muons, noSel, "noSel")
            plots+=cp.electronPlots(electrons, noSel, "noSel")
            plots+=cp.AK4jetPlots(ak4Jets, noSel, "noSel")
            plots+=cp.AK8jetPlots(tree.FatJet, noSel, "noSel")
            plots+=cp.AK8jetPlots(ak8Jets, noSel, "noSel_ak8jet")
            plots+=cp.AK8jetPlots(clak8Jets, noSel, "noSel_clak8jet")
            plots+=cp.AK4jetPlots(ak4JetsID, noSel, "noSelJetID")
            plots+=cp.AK4jetPlots(ak4Jetspt40, noSel, "noSelJetpt40")
            plots+=cp.eventPlots(tree, noSel, "noSel")
            
            ### no leptons
            plots+=cp.muonPlots(muons, noLepton, "noLEpton")
            plots+=cp.electronPlots(electrons, noLepton, "noLepton")



            ### dijet
            plots+=cp.muonPlots(muons, dijet, "Dijet")
            plots+=cp.electronPlots(electrons, dijet, "Dijet")

        ### dijet
        plots+=cp.AK4jetPlots(ak4Jets, dijet, "Dijet")
        plots+=cp.AK8jetPlots(ak8Jets, dijet, "Dijet")
        plots+=cp.AK4jetPlots(ak4JetsID, dijet, "DijetJetID")
        plots+=cp.AK4jetPlots(ak4Jetspt40, dijet, "DijetJetpt40")
        plots+=cp.AK4jetPlots(ak4Jetspt100, dijet, "DijetJetpt100")
        plots+=cp.AK4jetPlots(ak4Jetsetas2p4, dijet, "DijetJetetas2p4")
        plots+=cp.AK4jetPlots(ak4Jetsetag2p4, dijet, "DijetJetetag2p4")

        if sampleCfg['type'] == 'mc':  
            plots+=cp.effPurityPlots(clak4Jets,clak4genjets,clak4Jets, noSel,"effPurity", tree)

            if any([x in sampleCfg['plot_level'] for x in ["all","response"]]):
                plots+=cp.responsePlots( dijet, "dijet_AK4response", tree.GenJet, clak4Jets, tree, debug_hists= False)
                plots+=cp.responsePlots( dijet, "dijet_AK8response", tree.GenJet, clak8Jets, tree,debug_hists= False, deltaRcut = 0.4)

            if any([x in sampleCfg['plot_level'] for x in ["all","rawresponse"]]):
                plots+=cp.responsePlots( dijet, "dijet_AK4rawresponse", tree.GenJet, clak4Jets, tree, debug_hists= False, rawpt = True)
                plots+=cp.responsePlots( dijet, "dijet_AK8rawresponse", tree.GenJet, clak8Jets, tree, debug_hists= False, deltaRcut = 0.4, rawpt = True)

                plots+=cp.responsePlots( noSel, "noSel_AK4rawresponse", tree.GenJet, clak4Jets, tree, debug_hists= False, rawpt = True)
                plots+=cp.responsePlots( noSel, "noSel_AK8rawresponse", tree.GenJet, clak8Jets, tree, debug_hists= False, deltaRcut = 0.4, rawpt = True)


        plots+=cp.eventPlots(tree, dijet, "Dijet")
        plots+=cp.tauPlots(tree.GenVisTau, clak4Jets, noSel, "dijet_taueff_leadingtau0p4",ntaus = 1, deltaRcut = 0.4)
        plots+=cp.tauPlots(tree.GenVisTau, clak4Jets, noSel, "dijet_taueff_leadingtau0p2",ntaus = 1, deltaRcut = 0.2)
        plots+=cp.tauPlots(tree.GenVisTau, clak4Jets, noSel, "dijet_taueff_n3tau0p2",ntaus = 3, deltaRcut = 0.2)
        # Cutflow report
        # yields.add(noLepton, 'no lepton')
        yields.add(dijet, 'dijet')
        return plots

