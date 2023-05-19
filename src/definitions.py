from bamboo import treefunctions as op

# Object definitions


def muonDef(mu):
    return op.AND(
        mu.pt >= 35.,
        op.abs(mu.eta) <= 2.4,
        op.abs(mu.dxy) <= 0.05,
        op.abs(mu.dz) <= 0.1,
        mu.miniPFRelIso_all <= 0.4,
        mu.sip3d <= 8,
        mu.looseId
    )


def muonConePt(muons):
    return op.map(muons, lambda lep: op.multiSwitch(
        (op.AND(op.abs(lep.pdgId) != 11, op.abs(lep.pdgId) != 13), lep.pt),
        (op.AND(op.abs(lep.pdgId) == 13, lep.mvaTTH > 0.50), lep.pt),
        0.9*lep.pt*(1.+lep.jetRelIso)
    ))


def elDef(el):
    return op.AND(
        el.pt >= 35.,
        op.abs(el.eta) <= 2.5,
        op.abs(el.dxy) <= 0.05,
        op.abs(el.dz) <= 0.1,
        el.miniPFRelIso_all <= 0.4,
        el.sip3d <= 8,
        # el.mvaNoIso_WPL,
        el.lostHits <= 1
    )


def elConePt(electrons):
    return op.map(electrons, lambda lep: op.multiSwitch(
        (op.AND(op.abs(lep.pdgId) != 11, op.abs(lep.pdgId) != 13), lep.pt),
        # (op.AND(op.abs(lep.pdgId) == 11, lep.mvaTTH > 0.30), lep.pt), # run3 MC don't have mvaTTH for electrons
        (op.AND(op.abs(lep.pdgId) == 11), lep.pt),
        0.9*lep.pt*(1.+lep.jetRelIso)
    ))


def cleanElectrons(electrons, muons):
    cleanedElectrons = op.select(electrons, lambda el: op.NOT(
        op.rng_any(
            muons, lambda mu: op.deltaR(el.p4, mu.p4) <= 0.3))
    )
    return cleanedElectrons




def ak4jetDef(jet):
    return op.AND(
        #jet.jetId & 2,  # tight
        jet.pt > 20.,
        #op.abs(jet.eta) <= 2.4
    )

def cleanJets(jets, muons, electrons, sort=True):
    jets = op.select(jets, lambda jet: op.AND(
            op.NOT(op.rng_any(electrons, lambda ele: op.deltaR(jet.p4, ele.p4) < 0.4)),
            op.NOT(op.rng_any(muons, lambda mu: op.deltaR(jet.p4, mu.p4) < 0.4))
        ))
    if sort:
        jets = op.sort(jets, lambda j: -j.pt)
    return jets


def ak8jetDef(jet):
    return op.AND(
        #        jet.jetId & 2,  # tight
        jet.subJet1.isValid,
        jet.subJet2.isValid,
        jet.subJet1.pt > 20.,
        jet.subJet2.pt > 20.,
        op.abs(jet.subJet1.eta) <= 2.4,
        op.abs(jet.subJet2.eta) <= 2.4,
        jet.msoftdrop >= 30.,
        jet.msoftdrop <= 210.,
        jet.pt > 200.,
        op.abs(jet.eta) <= 2.4
    )

def effjets(jets):
    return op.select(jets,lambda jet: op.AND(
                op.deltaR(jet.p4,jet.genJet.p4) < 0.2,
                jet.genJet.pt > 30
            ))

def purityjets(jets):
    return op.select(jets, lambda jet: op.AND(
                op.deltaR(jet.p4,jet.genJet.p4) < 0.2,
                jet.genJet.pt > 20
            ))

def pujets(jets):
    return op.select(jets, lambda jet: 
                op.deltaR(jet.p4,jet.genJet.p4) > 0.4
            )

def matchedjets(jets):
    return  op.select(jets, lambda jet: op.AND( 
                jet.idx < 3,
                op.deltaR(jet.p4,jet.genJet.p4) < 0.2
            ))

def defineObjects(tree):
    # Muons
    muons = op.sort(
        op.select(tree.Muon, lambda mu: muonDef(mu)),
        #lambda mu: -muonConePt(tree.Muon)[mu.idx]
        lambda mu: -mu.pt
    )
    # Electrons
    electrons = op.sort(
        op.select(tree.Electron, lambda el: elDef(el)),
        #lambda el: -elConePt(tree.Electron)[el.idx]
        lambda el: -el.pt
    )
    # Cleaned Electrons
    clElectrons = cleanElectrons(electrons, muons)
    
    # AK4 Jets
    ak4Jets = op.sort(
        op.select(tree.Jet, lambda jet: ak4jetDef(jet)), lambda jet: -jet.pt)
    
    ## jet - lepton cleaning
    clak4Jets = cleanJets(ak4Jets, muons, clElectrons)
    
    ## jet ID & pT recommendations
    ak4JetsID = op.select(
        clak4Jets, lambda jet: jet.jetId & 2)
    
    ak4Jetspt40 = op.select(
        ak4JetsID, lambda jet: jet.pt > 40)

    ak4Jetspt100 = op.select(
        ak4JetsID, lambda jet: jet.pt > 100)
    
    ak4Jetsetas2p4 = op.select(
        ak4JetsID, lambda jet: op.abs(jet.eta) < 2.4)
    
    ak4Jetsetag2p4 = op.select(
        ak4JetsID, lambda jet: op.abs(jet.eta) > 2.4)


    return muons, electrons, clElectrons, ak4Jets, clak4Jets, ak4JetsID, ak4Jetspt40, ak4Jetspt100, ak4Jetsetas2p4, ak4Jetsetag2p4
    
