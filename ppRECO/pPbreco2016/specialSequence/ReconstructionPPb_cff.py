import FWCore.ParameterSet.Config as cms

### Beginning of Copy from Reconstruction_cff.py
##from Configuration.StandardSequences.Eras import eras

from RecoLuminosity.LumiProducer.lumiProducer_cff import *
from RecoLuminosity.LumiProducer.bunchSpacingProducer_cfi import *
from RecoLocalMuon.Configuration.RecoLocalMuon_cff import *
from RecoLocalCalo.Configuration.RecoLocalCalo_cff import *
from RecoTracker.Configuration.RecoTracker_cff import *
from RecoParticleFlow.PFClusterProducer.particleFlowCluster_cff import *
from TrackingTools.Configuration.TrackingTools_cff import *
from RecoTracker.MeasurementDet.MeasurementTrackerEventProducer_cfi import *
from RecoPixelVertexing.PixelLowPtUtilities.siPixelClusterShapeCache_cfi import *
siPixelClusterShapeCachePreSplitting = siPixelClusterShapeCache.clone(
    src = 'siPixelClustersPreSplitting'
    )

# Global  reco
from RecoEcal.Configuration.RecoEcal_cff import *
from RecoJets.Configuration.CaloTowersRec_cff import *
from RecoMET.Configuration.RecoMET_cff import *
from RecoMuon.Configuration.RecoMuon_cff import *
# Higher level objects
from RecoVertex.Configuration.RecoVertex_cff import *
from RecoEgamma.Configuration.RecoEgamma_cff import *
from RecoPixelVertexing.Configuration.RecoPixelVertexing_cff import *


from RecoJets.Configuration.RecoJetsGlobal_cff import *
from RecoMET.Configuration.RecoPFMET_cff import *
from RecoBTag.Configuration.RecoBTag_cff import *
#
# please understand that division global,highlevel is completely fake !
#
#local reconstruction
from RecoLocalTracker.Configuration.RecoLocalTracker_cff import *
from RecoParticleFlow.Configuration.RecoParticleFlow_cff import *
from RecoCTPPS.TotemRPLocal.totemRPLocalReconstruction_cff import *
#
# new tau configuration
#
from RecoTauTag.Configuration.RecoPFTauTag_cff import *
# Also BeamSpot
from RecoVertex.BeamSpotProducer.BeamSpot_cff import *

from RecoLocalCalo.CastorReco.CastorSimpleReconstructor_cfi import *

# Cosmic During Collisions
from RecoTracker.SpecialSeedGenerators.cosmicDC_cff import *

localreco = cms.Sequence(bunchSpacingProducer+trackerlocalreco+muonlocalreco+calolocalreco+castorreco)
localreco_HcalNZS = cms.Sequence(trackerlocalreco+muonlocalreco+calolocalrecoNZS+castorreco)

_ctpps_2016_localreco = localreco.copy()
_ctpps_2016_localreco += totemRPLocalReconstruction
eras.ctpps_2016.toReplaceWith(localreco, _ctpps_2016_localreco)

_ctpps_2016_localreco_HcalNZS = localreco_HcalNZS.copy()
_ctpps_2016_localreco_HcalNZS += totemRPLocalReconstruction
eras.ctpps_2016.toReplaceWith(localreco_HcalNZS, _ctpps_2016_localreco_HcalNZS)

#
# temporarily switching off recoGenJets; since this are MC and wil be moved to a proper sequence
#

from RecoLocalCalo.Castor.Castor_cff import *
from RecoLocalCalo.Configuration.hcalGlobalReco_cff import *

globalreco_tracking = cms.Sequence(offlineBeamSpot*
                          MeasurementTrackerEventPreSplitting* # unclear where to put this
                          siPixelClusterShapeCachePreSplitting* # unclear where to put this
                          standalonemuontracking*
                          trackingGlobalReco*
                          vertexreco)
_globalreco_tracking_LowPU_Phase1PU70 = globalreco_tracking.copy()
_globalreco_tracking_LowPU_Phase1PU70.replace(trackingGlobalReco, recopixelvertexing+trackingGlobalReco)
eras.trackingLowPU.toReplaceWith(globalreco_tracking, _globalreco_tracking_LowPU_Phase1PU70)
eras.trackingPhase1PU70.toReplaceWith(globalreco_tracking, _globalreco_tracking_LowPU_Phase1PU70)

globalreco = cms.Sequence(globalreco_tracking*
                          hcalGlobalRecoSequence*
                          particleFlowCluster*
                          ecalClusters*
                          caloTowersRec*                          
                          egammaGlobalReco*
                          jetGlobalReco*
                          muonGlobalReco*
                          pfTrackingGlobalReco*
                          muoncosmicreco*
                          CastorFullReco)

globalreco_plusPL= cms.Sequence(globalreco*ctfTracksPixelLess)

reducedRecHits = cms.Sequence ( reducedEcalRecHitsSequence * reducedHcalRecHitsSequence )

highlevelreco = cms.Sequence(egammaHighLevelRecoPrePF*
                             particleFlowReco*
                             egammaHighLevelRecoPostPF*
                             muoncosmichighlevelreco*
                             muonshighlevelreco *
                             particleFlowLinks*
                             jetHighLevelReco*
                             metrecoPlusHCALNoise*
                             btagging*
                             recoPFMET*
                             PFTau*
                             reducedRecHits*
                             cosmicDCTracksSeq
                             )

## Beginning of PPb reco
# PPb Event Characterization
from RecoHI.HiCentralityAlgos.HiCentrality_cfi import *
from RecoHI.HiCentralityAlgos.CentralityBin_cfi import *
from RecoHI.HiEvtPlaneAlgos.HiEvtPlane_cfi import *
# PPb Reco Sequence
ppbreco = cms.Sequence(hiCentrality
                       * centralityBin
                       * hiEvtPlane
                       )

## End of PPb reco

from FWCore.Modules.logErrorHarvester_cfi import *

# "Export" Section
## add "ppbreco" to "reconstruction"
reconstruction         = cms.Sequence(localreco*globalreco*highlevelreco*ppbreco*logErrorHarvester)

reconstruction_trackingOnly = cms.Sequence(localreco*globalreco_tracking)

#need a fully expanded sequence copy
modulesToRemove = list() # copy does not work well
noTrackingAndDependent = list()
noTrackingAndDependent.append(siPixelClustersPreSplitting)
noTrackingAndDependent.append(siStripZeroSuppression)
noTrackingAndDependent.append(siStripClusters)
noTrackingAndDependent.append(initialStepSeedLayersPreSplitting)
noTrackingAndDependent.append(initialStepSeedsPreSplitting)
noTrackingAndDependent.append(initialStepTrackCandidatesPreSplitting)
noTrackingAndDependent.append(initialStepTracksPreSplitting)
noTrackingAndDependent.append(firstStepPrimaryVerticesPreSplitting)
noTrackingAndDependent.append(initialStepTrackRefsForJetsPreSplitting)
noTrackingAndDependent.append(caloTowerForTrkPreSplitting)
noTrackingAndDependent.append(ak4CaloJetsForTrkPreSplitting)
noTrackingAndDependent.append(jetsForCoreTrackingPreSplitting)
noTrackingAndDependent.append(siPixelClusterShapeCachePreSplitting)
noTrackingAndDependent.append(siPixelClusters)
noTrackingAndDependent.append(clusterSummaryProducer)
noTrackingAndDependent.append(siPixelRecHitsPreSplitting)
noTrackingAndDependent.append(MeasurementTrackerEventPreSplitting)
noTrackingAndDependent.append(PixelLayerTriplets)
noTrackingAndDependent.append(pixelTracks)
noTrackingAndDependent.append(pixelVertices)
modulesToRemove.append(dt1DRecHits)
modulesToRemove.append(dt1DCosmicRecHits)
modulesToRemove.append(csc2DRecHits)
modulesToRemove.append(rpcRecHits)
#modulesToRemove.append(ecalGlobalUncalibRecHit)
modulesToRemove.append(ecalMultiFitUncalibRecHit)
modulesToRemove.append(ecalDetIdToBeRecovered)
modulesToRemove.append(ecalRecHit)
modulesToRemove.append(ecalCompactTrigPrim)
modulesToRemove.append(ecalTPSkim)
modulesToRemove.append(ecalPreshowerRecHit)
modulesToRemove.append(selectDigi)
modulesToRemove.append(hbheprereco)
modulesToRemove.append(hbhereco)
modulesToRemove.append(hfreco)
modulesToRemove.append(horeco)
modulesToRemove.append(hcalnoise)
modulesToRemove.append(zdcreco)
modulesToRemove.append(castorreco)
##it's OK according to Ronny modulesToRemove.append(CSCHaloData)#needs digis
reconstruction_fromRECO = reconstruction.copyAndExclude(modulesToRemove+noTrackingAndDependent)
noTrackingAndDependent.append(siPixelRecHitsPreSplitting)
noTrackingAndDependent.append(siStripMatchedRecHits)
noTrackingAndDependent.append(pixelTracks)
noTrackingAndDependent.append(ckftracks)
reconstruction_fromRECO_noTrackingTest = reconstruction.copyAndExclude(modulesToRemove+noTrackingAndDependent)
##requires generalTracks trajectories
noTrackingAndDependent.append(trackerDrivenElectronSeeds)
noTrackingAndDependent.append(ecalDrivenElectronSeeds)
noTrackingAndDependent.append(uncleanedOnlyElectronSeeds)
noTrackingAndDependent.append(uncleanedOnlyElectronCkfTrackCandidates)
noTrackingAndDependent.append(uncleanedOnlyElectronGsfTracks)
noTrackingAndDependent.append(uncleanedOnlyGeneralConversionTrackProducer)
noTrackingAndDependent.append(uncleanedOnlyGsfConversionTrackProducer)
noTrackingAndDependent.append(uncleanedOnlyPfTrackElec)
noTrackingAndDependent.append(uncleanedOnlyGsfElectronCores)
noTrackingAndDependent.append(uncleanedOnlyPfTrack)
noTrackingAndDependent.append(uncleanedOnlyGeneralInOutOutInConversionTrackMerger)#can live with
noTrackingAndDependent.append(uncleanedOnlyGsfGeneralInOutOutInConversionTrackMerger)#can live with
noTrackingAndDependent.append(uncleanedOnlyAllConversions)
noTrackingAndDependent.append(uncleanedOnlyGsfElectrons)#can live with
noTrackingAndDependent.append(electronMergedSeeds)
noTrackingAndDependent.append(electronCkfTrackCandidates)
noTrackingAndDependent.append(electronGsfTracks)
noTrackingAndDependent.append(generalConversionTrackProducer)
noTrackingAndDependent.append(generalInOutOutInConversionTrackMerger)
noTrackingAndDependent.append(gsfGeneralInOutOutInConversionTrackMerger)
noTrackingAndDependent.append(ecalDrivenGsfElectrons)
noTrackingAndDependent.append(gsfConversionTrackProducer)
noTrackingAndDependent.append(allConversions)
noTrackingAndDependent.append(gsfElectrons)
reconstruction_fromRECO_noTracking = reconstruction.copyAndExclude(modulesToRemove+noTrackingAndDependent)
reconstruction_noTracking = reconstruction.copyAndExclude(noTrackingAndDependent)


#sequences with additional stuff
reconstruction_withPixellessTk  = cms.Sequence(localreco        *globalreco_plusPL*highlevelreco*logErrorHarvester)
reconstruction_HcalNZS = cms.Sequence(localreco_HcalNZS*globalreco       *highlevelreco*logErrorHarvester)

#sequences without some stuffs
#
reconstruction_woCosmicMuons = cms.Sequence(localreco*globalreco*highlevelreco*logErrorHarvester)


# define a standard candle. please note I am picking up individual
# modules instead of sequences
#
reconstruction_standard_candle = cms.Sequence(localreco*globalreco*vertexreco*recoJetAssociations*btagging*electronSequence*photonSequence)
### End of Copy from Reconstruction_cff.py


#HF cleaning for data in the new design
# adding q tests for those lines            
#particleFlowRecHitHCAL.LongShortFibre_Cut = 30.
#particleFlowRecHitHCAL.ApplyPulseDPG = True


for qTest in particleFlowRecHitHF.producers[0].qualityTests:
    if qTest.name == 'PFRecHitQTestHCALChannel':
        qTest.maxSeverities.append(9)
        qTest.cleaningThresholds.append(30.)
        qTest.flags.append('HFDigi')
             

import RecoLocalCalo.HcalRecAlgos.RemoveAddSevLevel as HcalRemoveAddSevLevel
HcalRemoveAddSevLevel.AddFlag(hcalRecAlgos,"HFDigiTime",11)
HcalRemoveAddSevLevel.AddFlag(hcalRecAlgos,"HBHEFlatNoise",12)
HcalRemoveAddSevLevel.AddFlag(hcalRecAlgos,"HBHENegativeNoise",12)

CSCHaloData.ExpectedBX = cms.int32(3)

from JetMETCorrections.Configuration.JetCorrectors_cff import ak4PFCHSResidualCorrector, ak4PFCHSL1FastL2L3ResidualCorrector, ak4PFCHSL1FastL2L3ResidualCorrectorChain
jetCorrectorsForReco.replace(ak4PFCHSL1FastL2L3CorrectorChain, ak4PFCHSL1FastL2L3ResidualCorrectorChain)
