
from bamboo.plots import Plot, CutFlowReport
from bamboo.plots import EquidistantBinning as EqBin
from bamboo import treefunctions as op
from bamboo.analysisutils import forceDefine

import src.definitions as defs

from modules.baseModule import NanoBaseJME


class DYModule(NanoBaseJME):
    """"""

    def __init__(self, args):
        super(DYModule, self).__init__(args)

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

        # ak4bJets = op.select(
        #     ak4Jets, lambda jet: jet.btagDeepB > 0.2770)  # 2018 WP

        ### Di-leptonic channel ###

        # 2 muon and 2 electron selection
        hasTwoSFLeptons = noSel.refine('hasTwoSFLeptons', cut=(
            op.OR(
                op.AND(op.rng_len(muons) == 2, op.rng_len(clElectrons) ==0, 
                       muons[0].charge != muons[1].charge, 
                       muons[0].pt > 25., muons[1].pt > 15.),
                op.AND(op.rng_len(clElectrons) == 2, op.rng_len(muons) ==0,
                       clElectrons[0].charge != clElectrons[1].charge, 
                       clElectrons[0].pt > 25., clElectrons[1].pt > 15. )
            )
        ))



        # lepton channels
        # eePair = op.combine(clElectrons, N=2, pred=lambda el1,
        #                     el2: el1.charge != el2.charge)
        # mumuPair = op.combine(muons, N=2, pred=lambda mu1,
        #                       mu2: mu1.charge != mu2.charge)


        ### reconstruct Z boson
        Zboson = op.multiSwitch(
            (op.rng_len(muons)>0,op.sum(muons[0].p4,muons[1].p4)),
            (op.rng_len(clElectrons)>0,op.sum(clElectrons[0].p4,clElectrons[1].p4)),
            op.withMass(muons[0].p4,0)
        )

        ### Z mass selection
        Zmasscut = hasTwoSFLeptons.refine("Zmasscut", cut = (
                op.AND(Zboson.M() > 80, Zboson.M() < 100)
        ))


        #### deltaphi selection on jets

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

        ### two leptons
        plots+=cp.muonPlots(muons, hasTwoSFLeptons, "hasTwoSFLeptons")
        plots+=cp.electronPlots(electrons, hasTwoSFLeptons, "hasTwoSFLeptons")
        plots+=cp.ZbosonPlots(Zboson, hasTwoSFLeptons, "hasTwoSFLeptons")

        ### zmass cut
        plots+=cp.muonPlots(muons, Zmasscut, "Zmasscut")
        plots+=cp.electronPlots(electrons, Zmasscut, "Zmasscut")
        plots+=cp.ZbosonPlots(Zboson, Zmasscut, "Zmasscut")
        plots+=cp.AK4jetPlots(ak4Jets, Zmasscut, "Zmasscut")
        plots+=cp.AK4jetPlots(ak4JetsID, Zmasscut, "ZmasscutJetID")
        plots+=cp.AK4jetPlots(ak4Jetspt40, Zmasscut, "ZmasscutJetpt40")
        plots+=cp.AK4jetPlots(ak4Jetspt100, Zmasscut, "ZmasscutJetpt100")
        plots+=cp.AK4jetPlots(ak4Jetsetas2p4, Zmasscut, "ZmasscutJetetas2p4")
        plots+=cp.AK4jetPlots(ak4Jetsetag2p4, Zmasscut, "ZmasscutJetetag2p4")

        if sampleCfg['type'] == 'mc':  
            plots+=cp.effPurityPlots(effjets,Zmasscut,"effPurity_effmatched", tree)
            plots+=cp.effPurityPlots(recojetpt30,Zmasscut,"effPurity_allrecojets",tree)
            plots+=cp.effPurityPlots(purityjets,Zmasscut,"effPurity_puritymatched",tree)
            plots+=cp.effPurityPlots(pujets,Zmasscut,"effPurity_pujets",tree)

            plots+=cp.responsePlots(matchedjets, Zmasscut, "Zmasscut_response",tree)
            # plots+=cp.responsePlots(matchedjets, noLepton, "noLepton_response",tree)
            plots+=cp.responsePlots(matchedjets, noSel, "hasTwoSFLeptons_response",tree)

            plots+=cp.responsePlots(matchedjets, Zmasscut, "Zmasscut_rawresponse",tree, rawpt = True)
            # plots+=cp.responsePlots(matchedjets, noLepton, "noLepton_rawresponse",tree, rawpt = True)
            plots+=cp.responsePlots(matchedjets, noSel, "hasTwoSFLeptons_rawresponse",tree, rawpt = True)


            plots+=cp.AK4jetPlots(pujets, Zmasscut, "ZmasscutPuJets")
            plots+=cp.AK4jetPlots(matchedjets, Zmasscut, "ZmasscutMatchedJets")
            

        plots+=cp.eventPlots(tree, Zmasscut, "Zmasscut")
        # Cutflow report
        yields.add(hasTwoSFLeptons, 'two lepton')
        yields.add(Zmasscut, 'zmass cut')
        return plots
