#ref : Hadronizer_TuneCP5_13TeV_EEFilter_LHE_pythia8_cff.py
#import FWCore.ParameterSet.Config as cms

tautauFilter = cms.EDFilter("LHEGenericFilter",
    src = cms.InputTag("source"),
    NumRequired = cms.int32(2),
    ParticleID = cms.vint32(15),
    AcceptLogic = cms.string("EQ") # LT meaning < NumRequired, GT >, EQ =, NE !=
)           


ProductionFilterSequence = cms.Sequence(generator+tautauFilter)

