from bamboo.analysismodules import NanoAODModule, HistogramsModule
from bamboo.treedecorators import NanoAODDescription, CalcCollectionsGroups
from bamboo.analysisutils import makeMultiPrimaryDatasetTriggerSelection
from bamboo import treefunctions as op
from bamboo.analysisutils import forceDefine

from itertools import chain

from src.binnings import eta_binning, pt_binning, response_pt_binning
from bamboo.plots import Plot, CutFlowReport
from bamboo.plots import EquidistantBinning as EqBin
import src.definitions as defs
import src.controlPlots as cp


class NanoBaseJME(NanoAODModule, HistogramsModule):
    def __init__(self, args):
        super(NanoBaseJME, self).__init__(args)

    def addArgs(self, parser):
        super(NanoBaseJME, self).addArgs(parser)
        parser.add_argument("--era",
                            action='store',
                            type=str,
                            default=None,
                            help='This has no use right now!')

    def prepareTree(self, tree, sample=None, sampleCfg=None, backend=None):
        def isMC():
            if sampleCfg['type'] == 'data':
                return False
            elif sampleCfg['type'] == 'mc':
                return True
            else:
                raise RuntimeError(
                    f"The type '{sampleCfg['type']}' of {sample} dataset not understood.")
        
        self.is_MC = isMC()
        isDriver = (self.args.distributed == "driver")
        era = sampleCfg['era']  # reserved for future use
        campaign = sampleCfg['campaign']
        # jec = sampleCfg['jec']
        # jet_algo = 'AK4PFPuppi'
        # if jec=='':
        #     jec = 'Winter22Run3_V2_MC' if self.is_MC else 'Winter22Run3_RunD_V2_DATA'
        self.triggersPerPrimaryDataset = {}

        def addHLTPath(PD, HLT):
            if PD not in self.triggersPerPrimaryDataset.keys():
                self.triggersPerPrimaryDataset[PD] = []
            try:
                self.triggersPerPrimaryDataset[PD].append(
                    getattr(tree.HLT, HLT))
            except AttributeError:
                print("Couldn't find branch tree.HLT.%s, will omit it!" % HLT)

        def getNanoAODDescription():
            groups = ["HLT_", "MET_","PV_","Pileup_","Rho_"]
            collections = ["nElectron", "nJet", "nMuon", "nFatJet", "nSubJet","nGenJet"]
            varReaders = [CalcCollectionsGroups(Jet=("pt", "mass"))]
            return NanoAODDescription(groups=groups, collections=collections, systVariations=varReaders)

        tree, noSel, backend, lumiArgs = super(NanoBaseJME, self).prepareTree(tree=tree,
                                                                                 sample=sample,
                                                                                 sampleCfg=sampleCfg,
                                                                                 description=getNanoAODDescription(),
                                                                                 backend=backend)
        ### Triggers ###
        # Muon
        addHLTPath('Muon', 'IsoMu24')
        addHLTPath('Muon', 'IsoMu27')
        addHLTPath('Muon', 'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8')
        # EGamma
        addHLTPath('EGamma', 'Ele32_WPTight_Gsf')
        addHLTPath('EGamma', 'Ele23_Ele12_CaloIdL_TrackIdL_IsoVL')
        # MuonEG
        addHLTPath('MuonEG', 'Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')
        # SingleMuon
        addHLTPath('SingleMuon', 'IsoMu24')
        addHLTPath('SingleMuon', 'IsoMu27')
        # DoubleMuon
        addHLTPath('DoubleMuon', 'Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8')

        # JetHT
        addHLTPath('JetHT', 'DiPFJetAve40')
        addHLTPath('JetHT', 'DiPFJetAve60')
        addHLTPath('JetHT', 'DiPFJetAve80')
        addHLTPath('JetHT', 'DiPFJetAve140')
        addHLTPath('JetHT', 'DiPFJetAve200')
        addHLTPath('JetHT', 'DiPFJetAve260')
        addHLTPath('JetHT', 'DiPFJetAve320')
        addHLTPath('JetHT', 'DiPFJetAve400')
        addHLTPath('JetHT', 'DiPFJetAve500')
        addHLTPath('JetHT', 'DiPFJetAve60_HFJEC')
        addHLTPath('JetHT', 'DiPFJetAve80_HFJEC')
        addHLTPath('JetHT', 'DiPFJetAve100_HFJEC')
        addHLTPath('JetHT', 'DiPFJetAve160_HFJEC')
        addHLTPath('JetHT', 'DiPFJetAve220_HFJEC')
        addHLTPath('JetHT', 'DiPFJetAve300_HFJEC')

        # Gen Weight and Triggers
        if self.is_MC:
            noSel = noSel.refine('genWeight', weight=tree.genWeight, cut=(
                op.OR(*chain.from_iterable(self.triggersPerPrimaryDataset.values()))))
        else:
            noSel = noSel.refine('trigger', cut=[makeMultiPrimaryDatasetTriggerSelection(
                sample, self.triggersPerPrimaryDataset)])

        # #### reapply JECs ###
        # from bamboo.analysisutils import configureJets, configureType1MET
        # isNotWorker = (self.args.distributed != "worker") 
        # configureJets(tree._Jet, jet_algo,
        #               jec=jec,
        #               mayWriteCache= isNotWorker,
        #               jecLevels = sampleCfg['jec_level'],
        #               # cachedir='/afs/cern.ch/user/a/anmalara/workspace/WorkingArea/JME/jme-validation/JECs_2022/',
        #               isMC=self.is_MC, backend = backend)

        # configureType1MET(tree._MET,
        #     jec="Summer16_07Aug2017_V20_MC",
        #     smear="Summer16_25nsV1_MC",
        #     jesUncertaintySources=["Total"],
        #     mayWriteCache= not isDriver,
        #     isMC=self.isMC(sample), backend=be)

        # for calcProd in tree._Jet.calcProds:
        #     forceDefine(calcProd,noSel)

        return tree, noSel, backend, lumiArgs



class testModule(NanoBaseJME):
    def __init__(self, args):
        super(testModule, self).__init__(args)

    def definePlots(self, tree, noSel, sample=None, sampleCfg=None):
        plots = []
        yields = CutFlowReport("yields", printInLog=True, recursive=True)
        plots.append(yields)
        yields.add(noSel, 'No Selection')

        jets = op.sort(tree.Jet, lambda jet: -jet.genJet.pt)
        # plots.append(Plot.make1D(f"allfirstptjet", jets[0].pt,noSel,EqBin(100,0.,1000.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))
        jet = op.select(jets, lambda j:j.genJet.pt >= jets[3].genJet.pt)
        # plots.append(Plot.make1D(f"number", op.rng_len(jet),noSel,EqBin(5,0.,5.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))
        # plots.append(Plot.make1D(f"firstptjet", jet[0].pt,noSel,EqBin(100,0.,1000.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))
        jet_step2 = op.select(jet, lambda j:op.deltaR(j.p4,j.genJet.p4)<0.2)
        # plots.append(Plot.make1D(f"deltaR_firstptjet", jet_step2[0].pt,noSel,EqBin(100,0.,1000.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))
        # jet_step3 = op.select(jet_step2, lambda j:j.pt>30)
        # plots.append(Plot.make1D(f"pt30_firstptjet", jet_step3[0].pt,noSel,EqBin(100,0.,1000.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))


        #### selection einbauen
        #### mehr Stat laufen lassen
        #### in anderes Modul einbauen 
        #### JMENano fuer niedrigen PT cut

        for etatag,etabin in eta_binning.items():
            for pttag,ptbin in response_pt_binning.items():
                etaptjets = op.select(jet_step2, lambda j: op.AND(
                    op.abs(j.genJet.eta) > etabin[0],
                    op.abs(j.genJet.eta) < etabin[1],
                    j.genJet.pt > ptbin[0],
                    j.genJet.pt < ptbin[1]
                ))

                # plots.append(Plot.make1D(f"number2", op.rng_len(etaptjets),noSel,EqBin(5,0.,5.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))                

                noLepton = noSel.refine(f"noLepton_{etatag}_{pttag}", cut=(op.rng_len(etaptjets)>0))

                # plots.append(Plot.make1D(f"number3", op.rng_len(etaptjets),noLepton,EqBin(5,0.,5.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))                
                plots.append(Plot.make1D(f"ptjet_{etatag}_{pttag}", etaptjets[0].pt,noLepton,EqBin(100,0.,1000.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))
                plots.append(Plot.make1D(f"genptjet_{etatag}_{pttag}", etaptjets[0].genJet.pt,noLepton,EqBin(100,0.,1000.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))
                plots.append(Plot.make1D(f"etajet_{etatag}_{pttag}", etaptjets[0].eta,noLepton,EqBin(100,-5.,5.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))
                plots.append(Plot.make1D(f"genetajet_{etatag}_{pttag}", etaptjets[0].genJet.eta,noLepton,EqBin(100,-5.,5.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))
                plots.append(Plot.make1D(f"noSel_response_{etatag}_{pttag}", etaptjets[0].pt / etaptjets[0].genJet.pt,noLepton,EqBin(100,0.,3.),xTitle = "p_{T}^{reco}/p_{T}^{gen}"))

            #     break
            # break

        if sampleCfg['type'] == 'mc':  
            recojetpt30 = op.select(tree.Jet, lambda jet: jet.pt > 30)
            recojetpt20 = op.select(tree.Jet, lambda jet: jet.pt > 20)
            
            effjets = defs.effjets(recojetpt20)
            purityjets = defs.purityjets(recojetpt30)
        
            plots+=cp.effPurityPlots(effjets,noSel,"effPurity_effmatched", tree)
            plots+=cp.effPurityPlots(recojetpt30,noSel,"effPurity_allrecojets",tree)
            plots+=cp.effPurityPlots(purityjets,noSel,"effPurity_puritymatched",tree)
            # plots+=cp.effPurityPlots(pujets,dijet,"effPurity_pujets",tree)


        return plots
