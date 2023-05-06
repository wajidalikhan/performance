
from bamboo.plots import Plot, CutFlowReport
from bamboo.plots import EquidistantBinning as EqBin
from bamboo import treefunctions as op

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

        # Muons
        muons = op.sort(
            op.select(tree.Muon, lambda mu: defs.muonDef(mu)),
            #lambda mu: -defs.muonConePt(tree.Muon)[mu.idx]
            lambda mu: -mu.pt
        )
        # Electrons
        electrons = op.sort(
            op.select(tree.Electron, lambda el: defs.elDef(el)),
            #lambda el: -defs.elConePt(tree.Electron)[el.idx]
            lambda el: -el.pt
        )
        # Cleaned Electrons
        clElectrons = defs.cleanElectrons(electrons, muons)

        # AK8 Jets
        ak8Jets = op.sort(
            op.select(tree.FatJet, lambda jet: defs.ak8jetDef(jet)), lambda jet: -jet.pt)

        ak8JetsID = op.sort(
            ak8Jets, lambda jet: jet.jetId & 2)

        # AK4 Jets
        ak4Jets = op.sort(
            op.select(tree.Jet, lambda jet: defs.ak4jetDef(jet)), lambda jet: -jet.pt)

        ## jet - lepton cleaning
        #clak4Jets = defs.cleanJets(ak4Jets, muons, clElectrons)

        ## jet ID & pT recommendations
        ak4JetsID = op.select(
            ak4Jets, lambda jet: jet.jetId & 2)

        ak4Jetspt40 = op.select(
            ak4JetsID, lambda jet: jet.pt > 40)

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
        eePair = op.combine(clElectrons, N=2, pred=lambda el1,
                            el2: el1.charge != el2.charge)
        mumuPair = op.combine(muons, N=2, pred=lambda mu1,
                              mu2: mu1.charge != mu2.charge)


        firstEEpair = eePair[0]
        firstMUMUpair = mumuPair[0]

        ### reconstruct Z boson
        Zboson = op.multiSwitch(
            (op.rng_len(firstMUMUpair)==1,op.sum(firstMUMUpair[0].p4,firstMUMUpair[1].p4)),
            (op.rng_len(firstEEpair)==1,op.sum(firstEEpair[0].p4,firstEEpair[1].p4)),
            None
        )

        ### Z mass selection
        Zmasscut = hasTwoSFLeptons.refine("Zmasscut", cut = (
                op.AND(Zboson.M() > 80, Zboson.M() < 100)
        ))


        #### deltaphi selection on jets



        #############################################################################
        #                                 Plots                                     #
        #############################################################################
        import src.controlPlots as cp

        ### noSel
        plots+=cp.muonPlots(muons, noSel, "noSel")
        plots+=cp.electronPlots(electrons, noSel, "noSel")
        # plots+=cp.AK4jetPlots(ak4Jets, noSel, "noSel")
        # plots+=cp.AK4jetPlots(ak4JetsID, noSel, "noSelJetID")
        # plots+=cp.AK4jetPlots(ak4Jetspt40, noSel, "noSelJetpt40")

        ### two leptons
        # plots+=cp.muonPlots(muons, hasTwoSFLeptons, "hasTwoSFLeptons")
        # plots+=cp.electronPlots(electrons, hasTwoSFLeptons, "hasTwoSFLeptons")
        #plots+=cp.ZbosonPlots(Zboson, hasTwoSFLeptons, "hasTwoSFLeptons")

        ### zmass cut
        # plots+=cp.muonPlots(muons, Zmasscut, "Zmasscut")
        # plots+=cp.electronPlots(electrons, Zmasscut, "Zmasscut")
        #plots+=cp.ZbosonPlots(Zboson, Zmasscut, "Zmasscut")
        # plots+=cp.AK4jetPlots(ak4Jets, Zmasscut, "Zmasscut")
        # plots+=cp.AK4jetPlots(ak4JetsID, Zmasscut, "ZmasscutJetID")
        # plots+=cp.AK4jetPlots(ak4Jetspt40, Zmasscut, "ZmasscutJetpt40")

        # Cutflow report
        yields.add(hasTwoSFLeptons, 'two lepton')
        # yields.add(Zmasscut, 'zmass cut')
        return plots
