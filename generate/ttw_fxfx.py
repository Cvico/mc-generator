# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: GeneratorInterface/Pythia8Interface/python/fxfx.py --python_filename cfg_newLHE_newMatching.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAOD --fileout file:NanoGen_newLHE_newMatching.root --conditions 106X_upgrade2018_realistic_v4 --beamspot Realistic25ns13TeVEarly2018Collision --customise_commands process.source.numberEventsInLuminosityBlock=cms.untracked.uint32(161) --step LHE,GEN,NANOGEN --geometry DB:Extended --era Run2_2018 --no_exec --mc -n 30000
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing

from Configuration.Eras.Era_Run2_2018_cff import Run2_2018

options = VarParsing.VarParsing()

options.register('outpath',
                 './',      #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Out folder")

options.register('outname',
                 "TTWJetsToLNu_fxfx_v2",
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "The outname")

options.register('gridpack',
                  #'/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/TTWJetsToLNu_5f_NLO_FXFX/TTWJetsToLNu_5f_NLO_FXFX_slc7_amd64_gcc700_CMSSW_10_6_0_tarball.tar.xz',
                 '/pool/phedex/userstorage/cvico/ttw-diff/gridpack_TTW_fxfx/v2/TTWJetsToLNu_5f_NLO_FXFX_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz',
                 #"/pool/phedex/userstorage/cvico/ttw-diff/gridpack_TTW_fxfx/v3_ptj20/TTWJetsToLNu_5f_NLO_FXFX_slc7_amd64_gcc900_CMSSW_12_0_2_tarball.tar.xz",
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "The gridpack")

options.register('ncores',
                 1,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Ncores")

options.register('nevs',
                 10,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Nevs")

options.register('seed',
                 444444,
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "seed")

options.parseArguments()

process = cms.Process('NANOGEN',Run2_2018)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeVEarly2018Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('PhysicsTools.NanoAOD.nanogen_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.nevs),
)
#### Random numbers
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
    saveFileName = cms.untracked.string(''),
    externalLHEProducer = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    generator = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    Pythia8ConcurrentHadronizerFilter = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    Pythia8HadronizerFilter = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    CTPPSFastRecHits = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    LHCTransport = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    MuonSimHits = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    VtxSmeared = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    ecalPreshowerRecHit = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    ecalRecHit = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    famosPileUp = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    fastSimProducer = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    fastTrackerRecHits = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    g4SimHits = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    hbhereco = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    hfreco = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    hiSignal = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    hiSignalG4SimHits = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    hiSignalLHCTransport = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    horeco = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    l1ParamMuons = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    mix = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    mixData = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    mixGenPU = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    mixRecoTracks = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    mixSimCaloHits = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    paramMuons = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    simBeamSpotFilter = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    simMuonCSCDigis = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    simMuonDTDigis = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    simMuonGEMDigis = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    simMuonRPCDigis = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    ),
    simSiStripDigiSimLink = cms.PSet(
        initialSeed = cms.untracked.uint32(options.seed)
    )
)


# Input source
process.source = cms.Source("EmptySource")


process.options = cms.untracked.PSet(
    FailPath = cms.untracked.vstring(),
    IgnoreCompletely = cms.untracked.vstring(),
    Rethrow = cms.untracked.vstring(),
    SkipEvent = cms.untracked.vstring(),
    allowUnscheduled = cms.obsolete.untracked.bool,
    canDeleteEarly = cms.untracked.vstring(),
    deleteNonConsumedUnscheduledModules = cms.untracked.bool(True),
    dumpOptions = cms.untracked.bool(False),
    emptyRunLumiMode = cms.obsolete.untracked.string,
    eventSetup = cms.untracked.PSet(
        forceNumberOfConcurrentIOVs = cms.untracked.PSet(
            allowAnyLabel_=cms.required.untracked.uint32
        ),
        numberOfConcurrentIOVs = cms.untracked.uint32(0)
    ),
    fileMode = cms.untracked.string('FULLMERGE'),
    forceEventSetupCacheClearOnNewRun = cms.untracked.bool(False),
    makeTriggerResults = cms.obsolete.untracked.bool,
    numberOfConcurrentLuminosityBlocks = cms.untracked.uint32(0),
    numberOfConcurrentRuns = cms.untracked.uint32(1),
    numberOfStreams = cms.untracked.uint32(0),
    numberOfThreads = cms.untracked.uint32(1),
    printDependencies = cms.untracked.bool(False),
    sizeOfStackForThreadsInKB = cms.optional.untracked.uint32,
    throwIfIllegalParameter = cms.untracked.bool(True),
    wantSummary = cms.untracked.bool(False)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('Configuration/GenProduction/python/ttX-fxfx-fragment.py nevts:' + str(options.nevs)),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    ),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAOD'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:%s'%options.outname),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2018_realistic_v4', '')

process.generator = cms.EDFilter("Pythia8HadronizerFilter",
    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP5Settings',
            'pythia8aMCatNLOSettings',
            'pythia8PSweightsSettings',
            'processParameters'
        ),
        processParameters = cms.vstring(
            'JetMatching:setMad = off',
            'JetMatching:scheme = 1',
            'JetMatching:doVeto = off',
            'JetMatching:merge = on',
            'JetMatching:jetAlgorithm = 2',
            'JetMatching:etaJetMax = 1000',
            'JetMatching:coneRadius = 1.',
            'JetMatching:slowJetPower = 1',
            'JetMatching:qCut = 150.',
            'JetMatching:doFxFx = on',
            'JetMatching:qCutME = 60.',
            'JetMatching:nQmatch = 5',
            'JetMatching:nJetMax = 1'
        ),
        pythia8CP5Settings = cms.vstring(
            'Tune:pp 14',
            'Tune:ee 7',
            'MultipartonInteractions:ecmPow=0.03344',
            'MultipartonInteractions:bProfile=2',
            'MultipartonInteractions:pT0Ref=1.41',
            'MultipartonInteractions:coreRadius=0.7634',
            'MultipartonInteractions:coreFraction=0.63',
            'ColourReconnection:range=5.176',
            'SigmaTotal:zeroAXB=off',
            'SpaceShower:alphaSorder=2',
            'SpaceShower:alphaSvalue=0.118',
            'SigmaProcess:alphaSvalue=0.118',
            'SigmaProcess:alphaSorder=2',
            'MultipartonInteractions:alphaSvalue=0.118',
            'MultipartonInteractions:alphaSorder=2',
            'TimeShower:alphaSorder=2',
            'TimeShower:alphaSvalue=0.118',
            'SigmaTotal:mode = 0',
            'SigmaTotal:sigmaEl = 21.89',
            'SigmaTotal:sigmaTot = 100.309',
            'PDF:pSet=LHAPDF6:NNPDF31_nnlo_as_0118'
        ),
        pythia8CommonSettings = cms.vstring(
            'Tune:preferLHAPDF = 2',
            'Main:timesAllowErrors = 10000',
            'Check:epTolErr = 0.01',
            'Beams:setProductionScalesFromLHEF = on',
            'SLHA:minMassSM = 1000.',
            'ParticleDecays:limitTau0 = on',
            'ParticleDecays:tau0Max = 10',
            'ParticleDecays:allowPhotonRadiation = on'
        ),
        pythia8PSweightsSettings = cms.vstring(
            'UncertaintyBands:doVariations = on',
            'UncertaintyBands:List = {isrRedHi isr:muRfac=0.707,fsrRedHi fsr:muRfac=0.707,isrRedLo isr:muRfac=1.414,fsrRedLo fsr:muRfac=1.414,isrDefHi isr:muRfac=0.5,fsrDefHi fsr:muRfac=0.5,isrDefLo isr:muRfac=2.0,fsrDefLo fsr:muRfac=2.0,isrConHi isr:muRfac=0.25,fsrConHi fsr:muRfac=0.25,isrConLo isr:muRfac=4.0,fsrConLo fsr:muRfac=4.0,fsr_G2GG_muR_dn fsr:G2GG:muRfac=0.5,fsr_G2GG_muR_up fsr:G2GG:muRfac=2.0,fsr_G2QQ_muR_dn fsr:G2QQ:muRfac=0.5,fsr_G2QQ_muR_up fsr:G2QQ:muRfac=2.0,fsr_Q2QG_muR_dn fsr:Q2QG:muRfac=0.5,fsr_Q2QG_muR_up fsr:Q2QG:muRfac=2.0,fsr_X2XG_muR_dn fsr:X2XG:muRfac=0.5,fsr_X2XG_muR_up fsr:X2XG:muRfac=2.0,fsr_G2GG_cNS_dn fsr:G2GG:cNS=-2.0,fsr_G2GG_cNS_up fsr:G2GG:cNS=2.0,fsr_G2QQ_cNS_dn fsr:G2QQ:cNS=-2.0,fsr_G2QQ_cNS_up fsr:G2QQ:cNS=2.0,fsr_Q2QG_cNS_dn fsr:Q2QG:cNS=-2.0,fsr_Q2QG_cNS_up fsr:Q2QG:cNS=2.0,fsr_X2XG_cNS_dn fsr:X2XG:cNS=-2.0,fsr_X2XG_cNS_up fsr:X2XG:cNS=2.0,isr_G2GG_muR_dn isr:G2GG:muRfac=0.5,isr_G2GG_muR_up isr:G2GG:muRfac=2.0,isr_G2QQ_muR_dn isr:G2QQ:muRfac=0.5,isr_G2QQ_muR_up isr:G2QQ:muRfac=2.0,isr_Q2QG_muR_dn isr:Q2QG:muRfac=0.5,isr_Q2QG_muR_up isr:Q2QG:muRfac=2.0,isr_X2XG_muR_dn isr:X2XG:muRfac=0.5,isr_X2XG_muR_up isr:X2XG:muRfac=2.0,isr_G2GG_cNS_dn isr:G2GG:cNS=-2.0,isr_G2GG_cNS_up isr:G2GG:cNS=2.0,isr_G2QQ_cNS_dn isr:G2QQ:cNS=-2.0,isr_G2QQ_cNS_up isr:G2QQ:cNS=2.0,isr_Q2QG_cNS_dn isr:Q2QG:cNS=-2.0,isr_Q2QG_cNS_up isr:Q2QG:cNS=2.0,isr_X2XG_cNS_dn isr:X2XG:cNS=-2.0,isr_X2XG_cNS_up isr:X2XG:cNS=2.0}',
            'UncertaintyBands:nFlavQ = 4',
            'UncertaintyBands:MPIshowers = on',
            'UncertaintyBands:overSampleFSR = 10.0',
            'UncertaintyBands:overSampleISR = 10.0',
            'UncertaintyBands:FSRpTmin2Fac = 20',
            'UncertaintyBands:ISRpTmin2Fac = 1'
        ),
        pythia8aMCatNLOSettings = cms.vstring(
            'SpaceShower:pTmaxMatch = 1',
            'SpaceShower:pTmaxFudge = 1',
            'SpaceShower:MEcorrections = off',
            'TimeShower:pTmaxMatch = 1',
            'TimeShower:pTmaxFudge = 1',
            'TimeShower:MEcorrections = off',
            'TimeShower:globalRecoil = on',
            'TimeShower:limitPTmaxGlobal = on',
            'TimeShower:nMaxGlobalRecoil = 1',
            'TimeShower:globalRecoilMode = 2',
            'TimeShower:nMaxGlobalBranch = 1',
            'TimeShower:weightGluonToQuark = 1'
        )
    ),
    UserCustomization = cms.VPSet(cms.PSet(
        pluginName = cms.string('JetMatchingNewFxFx')
    )),
    comEnergy = cms.double(13000.0),
    filterEfficiency = cms.untracked.double(1.0),
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(1)
)


process.externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring(options.gridpack),
    generateConcurrently = cms.untracked.bool(True),
    nEvents = cms.untracked.uint32(options.nevs),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)




# Path and EndPath definitions
process.lhe_step = cms.Path(process.externalLHEProducer)
process.generation_step = cms.Path(process.pgen)
process.nanoAOD_step = cms.Path(process.nanogenSequence)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.lhe_step,process.generation_step,process.genfiltersummary_step,process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)
# filter all path with the production filter sequence
for path in process.paths:
	if path in ['lhe_step']: continue
	getattr(process,path).insert(0, process.generator)

# customisation of the process.
# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nanogen_cff
from PhysicsTools.NanoAOD.nanogen_cff import customizeNanoGEN 

#call to customisation function customizeNanoGEN imported from PhysicsTools.NanoAOD.nanogen_cff
process = customizeNanoGEN(process)
process.genJetTable.src = "ak4GenJetsNoNu"
process.genJetAK8Table.src = "ak8GenJetsNoNu"

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions


# Customisation from command line

process.source.numberEventsInLuminosityBlock=cms.untracked.uint32(options.nevs)
# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
