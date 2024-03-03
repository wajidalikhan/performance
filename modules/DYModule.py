
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


        muons, electrons, clElectrons, ak4Jets, clak4Jets, ak4JetsID, ak4Jetspt40, ak4Jetspt100, ak4Jetsetas2p4, ak4Jetsetag2p4, ak8Jets, clak8Jets, clak4genjets = defs.defineObjects(tree)


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
            # recojetpt30 = op.select(ak4Jets, lambda jet: jet.pt > 30)
            # recojetpt20 = op.select(ak4Jets, lambda jet: jet.pt > 20)
            
            # effjets = defs.effjets(recojetpt20)

            # purityjets = defs.purityjets(recojetpt30)
            
            pujets = defs.pujets(ak4Jets)

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
            plots+=cp.effPurityPlots(clak4Jets,clak4genjets,clak4Jets,Zmasscut,"effPurity", tree)

            if any([x in sampleCfg['plot_level'] for x in ["all","response"]]): 
                plots+=cp.responsePlots( Zmasscut, "Zmasscut_AK4response", tree.GenJet, clak4Jets, tree, debug_hists= False)
                plots+=cp.responsePlots( Zmasscut, "Zmasscut_AK8response", tree.GenJet, clak8Jets, tree, debug_hists= False, deltaRcut = 0.4)

                plots+=cp.responsePlots( noSel, "noSel_AK4response", tree.GenJet, clak4Jets, tree, debug_hists= False)
                plots+=cp.responsePlots( noSel, "noSel_AK8response", tree.GenJet, clak8Jets, tree, debug_hists= False, deltaRcut = 0.4)

            if any([x in sampleCfg['plot_level'] for x in ["all","rawresponse"]]):
                plots+=cp.responsePlots( Zmasscut, "Zmasscut_AK4rawresponse", tree.GenJet, clak4Jets, tree, debug_hists= False, rawpt = True)
                plots+=cp.responsePlots( Zmasscut, "Zmasscut_AK8rawresponse", tree.GenJet, clak8Jets, tree, debug_hists= False, deltaRcut = 0.4, rawpt = True)

                plots+=cp.responsePlots( noSel, "noSel_AK4rawresponse", tree.GenJet, clak4Jets, tree, debug_hists= False, rawpt = True)
                plots+=cp.responsePlots( noSel, "noSel_AK8rawresponse", tree.GenJet, clak8Jets, tree, debug_hists= False, deltaRcut = 0.4, rawpt = True)


            plots+=cp.AK4jetPlots(pujets, Zmasscut, "ZmasscutPuJets")
            

        #Hadronic tau decay mode. 0=OneProng0PiZero, 1=OneProng1PiZero, 2=OneProng2PiZero, 10=ThreeProng0PiZero, 11=ThreeProng1PiZero, 15=Other
        taustati = [0,1,2,10,11,15]

        plots+=cp.tauPlots(tree.GenVisTau, tree.Jet, noSel, "noJetSel_taueff_leadingtau0p4",ntaus = 1, deltaRcut = 0.4)
        plots+=cp.tauPlots(tree.GenVisTau, tree.Jet,  noSel, "noJetSel_taueff_leadingtau0p2",ntaus = 1, deltaRcut = 0.2)

        for status in taustati:
            plots+=cp.tauPlots(op.select(tree.GenVisTau, lambda tau: tau.status ==status), tree.Jet,  noSel, "noJetSeltaustatus"+str(status)+"_taueff_leadingtau0p2",ntaus = 1, deltaRcut = 0.2)

        if sampleCfg['withCHS']:
            plots+=cp.tauPlots(tree.GenVisTau, tree.JetCHS, noSel, "noJetSelCHS_taueff_leadingtau0p2",ntaus = 1, deltaRcut = 0.2)

            for status in taustati:
                plots+=cp.tauPlots(op.select(tree.GenVisTau, lambda tau: tau.status ==status), tree.JetCHS,  noSel, "noJetSeltaustatus"+str(status)+"CHS_taueff_leadingtau0p2",ntaus = 1, deltaRcut = 0.2)


        plots+=cp.tauPlots(tree.GenVisTau, tree.Tau, noSel, "noJetSelTau_taueff_leadingtau0p2",ntaus = 1, deltaRcut = 0.2, bPNet = False)
        for status in taustati:
            plots+=cp.tauPlots(op.select(tree.GenVisTau, lambda tau: tau.status ==status), tree.Tau,  noSel, "noJetSeltaustatus"+str(status)+"Tau_taueff_leadingtau0p2",ntaus = 1, deltaRcut = 0.2, bPNet = False)

        plots+=cp.tauPlots(tree.GenVisTau, tree.GenJet, noSel, "noJetSelGenJet_taueff_leadingtau0p2",ntaus = 1, deltaRcut = 0.2, bPNet = False)
        for status in taustati:
            plots+=cp.tauPlots(op.select(tree.GenVisTau, lambda tau: tau.status ==status), tree.GenJet,  noSel, "noJetSeltaustatus"+str(status)+"GenJet_taueff_leadingtau0p2",ntaus = 1, deltaRcut = 0.2, bPNet = False)


        plots+=cp.eventPlots(tree, Zmasscut, "Zmasscut")
        # Cutflow report
        yields.add(hasTwoSFLeptons, 'two lepton')
        yields.add(Zmasscut, 'zmass cut')
        return plots
