from bamboo.analysismodules import NanoAODModule, HistogramsModule
from bamboo.treedecorators import NanoAODDescription, CalcCollectionsGroups
from bamboo.analysisutils import makeMultiPrimaryDatasetTriggerSelection
from bamboo import treefunctions as op
from bamboo.analysisutils import forceDefine

from itertools import chain

from src.binnings import eta_binning, pt_binning, response_pt_binning
from bamboo.plots import Plot, CutFlowReport,  SummedPlot
from bamboo.plots import EquidistantBinning as EqB
from bamboo.plots import VariableBinning as VarBin
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
            varReaders = [CalcCollectionsGroups(Jet=("pt", "mass")),CalcCollectionsGroups(FatJet=("pt", "mass","msoftdrop"))]
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
            # noSel = noSel.refine('genWeight', weight=tree.genWeight, cut=(
            #     op.OR(*chain.from_iterable(self.triggersPerPrimaryDataset.values()))))
            noSel = noSel.refine('genWeight', weight=tree.genWeight)
          
          
        else:
            noSel = noSel.refine('trigger', cut=[makeMultiPrimaryDatasetTriggerSelection(
                sample, self.triggersPerPrimaryDataset)])

        return tree, noSel, backend, lumiArgs



class testModule(NanoBaseJME):
    def __init__(self, args):
        super(testModule, self).__init__(args)

    def definePlots(self, tree, noSel, sample=None, sampleCfg=None):
        plots = []
        yields = CutFlowReport("yields", printInLog=True, recursive=True)
        plots.append(yields)
        yields.add(noSel, 'No Selection')


        plots.append(Plot.make1D(f"noSel_AK8Jets_nJets",op.rng_len(tree.FatJet),noSel,EqB(15,0.,15.), xTitle=f"Number of Jets"))

        muons = op.select(tree.Muon, lambda mu: op.AND(mu.pt > 20., op.abs(mu.eta) < 2.4))
        electrons = op.select(tree.Electron, lambda el: op.AND(el.pt > 20, op.abs(el.eta) < 2.5))
        jets_noclean = op.select(tree.Jet, lambda j: op.AND(j.jetId & 0x2, op.abs(j.eta) < 5.2, j.pt > 5.))
        jets = op.sort(
            op.select(jets_noclean, lambda j: op.AND(
                op.NOT(op.rng_any(muons, lambda l: op.deltaR(l.p4, j.p4) < 0.4)),
                op.NOT(op.rng_any(electrons, lambda l: op.deltaR(l.p4, j.p4) < 0.4))
            )), lambda j: -j.pt)

        dijetSel = noSel.refine("dijetSelection", cut=[op.rng_len(jets)>=1])#, op.deltaPhi(jets[0].p4, jets[1].p4)>2.7])

        genjets = op.sort(tree.GenJet, lambda j: -j.pt)
        etaBinning = [etabin[0] for etatag, etabin in eta_binning.items()]
        etaBinning = etaBinning[:-1]
        etaBinning = VarBin(etaBinning)

        ptBinning = VarBin([ptbin[0] for pttag, ptbin in response_pt_binning.items()])

        for ix in range(3):
            genjet = genjets[ix]
            recojet = op.rng_min_element_by(jets, lambda jet: op.deltaR(jet.p4,genjet.p4))
            if ix == 0:
                ratio0 = Plot.make3D("ratio_0", (op.switch(op.AND(op.rng_len(genjets)>ix,op.deltaR(recojet.p4,genjet.p4)<0.2, op.rng_len(jets)>0),recojet.pt/genjet.pt, -99.), genjet.pt, op.abs(genjet.eta)) , dijetSel, (EqB(100, 0., 2.),ptBinning, etaBinning), xTitle="Response", yTitle="pt", zTitle="eta")
                plots.append(ratio0)
            if ix == 1:
                ratio1 = Plot.make3D("ratio_1", (op.switch(op.AND(op.rng_len(genjets)>ix,op.deltaR(recojet.p4,genjet.p4)<0.2, op.rng_len(jets)>0),recojet.pt/genjet.pt, -99.), genjet.pt, op.abs(genjet.eta)), dijetSel, (EqB(100, 0., 2.),ptBinning, etaBinning), xTitle="Response", yTitle="pt", zTitle="eta")
                plots.append(ratio1)
            if ix == 2:
                ratio2 = Plot.make3D("ratio_2", (op.switch(op.AND(op.rng_len(genjets)>ix,op.deltaR(recojet.p4,genjet.p4)<0.2, op.rng_len(jets)>0),recojet.pt/genjet.pt, -99.), genjet.pt, op.abs(genjet.eta)), dijetSel, (EqB(100, 0., 2.),ptBinning, etaBinning), xTitle="Response", yTitle="pt", zTitle="eta")
                plots.append(ratio2)

            jets = op.select(jets, lambda j: j.idx!=recojet.idx)

        plots.append(SummedPlot("ratio", [ratio0, ratio1, ratio2], xTitle="Response for 3 jets",yTitle="pt", zTitle="eta"))


        return plots
