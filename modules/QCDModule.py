
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


        # # AK8 Jets
        # ak8Jets = op.sort(
        #     op.select(tree.FatJet, lambda jet: defs.ak8jetDef(jet)), lambda jet: -jet.pt)

        # ak8JetsID = op.sort(
        #     ak8Jets, lambda jet: jet.jetId & 2)


        muons, electrons, clElectrons, ak4Jets, clak4Jets, ak4JetsID, ak4Jetspt40, ak4Jetspt100, ak4Jetsetas2p4, ak4Jetsetag2p4 = defs.defineObjects(tree)

        ### dijet selection
        noLepton = noSel.refine("noLepton", cut=(
            op.AND(
                op.rng_len(muons) == 0,
                op.rng_len(clElectrons) ==0
            )))


        dijet = noLepton.refine("dijet", cut = (
            op.AND(
                op.rng_len(clak4Jets)>1,
                clak4Jets[0].pt > 50,
                op.deltaPhi(clak4Jets[0].p4,clak4Jets[1].p4)>2.7
            )))
        

        if sampleCfg['type'] == 'mc':
            #### efficiency and purity
            ### efficiency match to generator jets with deltaR<0.2 and pT gen >30, pt reco > 20
            recojetpt30 = op.select(ak4Jets, lambda jet: jet.pt > 30)
            recojetpt20 = op.select(ak4Jets, lambda jet: jet.pt > 20)
            
            # firstgenjet = tree.Jet[0].chHEF
            
            effjets = defs.effjets(recojetpt20)

            purityjets = defs.purityjets(recojetpt30)
            
            pujets = defs.pujets(ak4Jets)

            matchedjets = defs.matchedjets(tree.Jet)

        #############################################################################
        #                                 Plots                                     #
        #############################################################################
        import src.controlPlots as cp

        ### noSel
        plots+=cp.muonPlots(muons, noSel, "noSel")
        plots+=cp.electronPlots(electrons, noSel, "noSel")
        plots+=cp.AK4jetPlots(ak4Jets, noSel, "noSel")
        plots+=cp.AK4jetPlots(ak4JetsID, noSel, "noSelJetID")
        plots+=cp.AK4jetPlots(ak4Jetspt40, noSel, "noSelJetpt40")
        plots+=cp.eventPlots(tree, noSel, "noSel")

        ### no leptons
        plots+=cp.muonPlots(muons, noLepton, "noLEpton")
        plots+=cp.electronPlots(electrons, noLepton, "noLepton")


        ### zmass cut
        plots+=cp.muonPlots(muons, dijet, "Dijet")
        plots+=cp.electronPlots(electrons, dijet, "Dijet")
        plots+=cp.AK4jetPlots(ak4Jets, dijet, "Dijet")
        plots+=cp.AK4jetPlots(ak4JetsID, dijet, "DijetJetID")
        plots+=cp.AK4jetPlots(ak4Jetspt40, dijet, "DijetJetpt40")
        plots+=cp.AK4jetPlots(ak4Jetspt100, dijet, "DijetJetpt100")
        plots+=cp.AK4jetPlots(ak4Jetsetas2p4, dijet, "DijetJetetas2p4")
        plots+=cp.AK4jetPlots(ak4Jetsetag2p4, dijet, "DijetJetetag2p4")

        if sampleCfg['type'] == 'mc':  
            plots+=cp.effPurityPlots(effjets,dijet,"effPurity_effmatched", tree)
            plots+=cp.effPurityPlots(ak4Jets,dijet,"effPurity_allrecojets",tree)
            plots+=cp.effPurityPlots(purityjets,dijet,"effPurity_puritymatched",tree)
            plots+=cp.effPurityPlots(pujets,dijet,"effPurity_pujets",tree)

            plots+=cp.responsePlots(matchedjets, dijet, "response",tree)

        plots+=cp.eventPlots(tree, dijet, "Dijet")
        # Cutflow report
        yields.add(noLepton, 'no lepton')
        yields.add(dijet, 'dijet')
        return plots

