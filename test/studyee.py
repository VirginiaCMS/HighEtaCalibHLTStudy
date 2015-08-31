#!/bin/python

# Initial example scripts for HighEta HLT studies
# Contact: Hengne.Li@cern.ch 
# 11 Aug. 2015
# modified to match the DYEE sample which was shown in the ppt.
# modified to cut both the inital and final ee daughters .   Aug21.2015
import sys, os, string, re, pwd, commands, ast, optparse, shlex, time
import ROOT
import itertools
import math
from DataFormats.FWLite import Events, Handle
from array import array



grootargs = []
def callback_rootargs(option, opt, value, parser):
    grootargs.append(opt)

### Define function for parsing options
def parseOptions():

    global opt, args, runAllSteps

    usage = ('usage: %prog [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    # input options
    parser.add_option("-l",action="callback",callback=callback_rootargs)
    parser.add_option("-q",action="callback",callback=callback_rootargs)
    parser.add_option("-b",action="callback",callback=callback_rootargs)

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()

#### 
def printDaughter(part,dent):
    ndau = part.numberOfDaughters()
    for id in range(0,ndau):
        dpart = part.daughter(id)
        adent = "  "+dent
        print adent,"pdg=",dpart.pdgId(),"; status=",dpart.status(),"; ndau=",dpart.numberOfDaughters()
        if part.numberOfDaughters()>0 : 
            printDaughter(dpart,adent)

#### 
def getStatusOneDaughter(part,pdgid):
    ndau = part.numberOfDaughters()
    for id in range(0,ndau):
        dpart = part.daughter(id)
        if abs(dpart.pdgId())!=pdgid: continue
        if dpart.status()==1: return dpart
        else: return getStatusOneDaughter(dpart,pdgid)
        


# parse the arguments and options
global opt, args, runAllSteps
parseOptions()
sys.argv = grootargs


genParticles  = Handle  ('std::vector<reco::GenParticle>')

# input 
events = Events(['root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/06911F9F-9899-E411-B576-001E67396ACC.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/1676BF69-8E99-E411-8544-001E673976D9.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/24BB002C-A199-E411-A815-001E67397E13.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/2CFB8725-9299-E411-BB74-001E67396DCE.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/32893EE9-9C99-E411-A6ED-001E67397CB0.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/340FA3FA-9E99-E411-AB36-002481E7451E.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/3469A594-A399-E411-B3C5-001E67396DEC.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/3A36CC7C-8A99-E411-9CE1-002590200850.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/4028711D-A299-E411-8FCD-002481E14F86.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/4A9ECB16-A699-E411-8EF6-001E6739689C.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/4E74DD7B-9B99-E411-B71A-002590A8882C.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/76B77414-9C99-E411-B2EC-002590200B78.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/7EDE5E7E-A099-E411-BC3E-001E67398CAA.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/807C3BDD-A199-E411-9CD9-0025B31E330A.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/80AAB1DB-A999-E411-BE33-001E67397747.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/80AFDE8D-9399-E411-AA79-002590200B10.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/882A30D0-9F99-E411-AFD3-001E67396E64.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/8A469B23-9699-E411-B55C-001E67398412.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/929CE4D7-8F99-E411-B056-002590200840.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/92CCDEEF-A299-E411-AEB9-002590200B34.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/98EBF4AC-A099-E411-B998-001E67396644.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/A208DDEB-9899-E411-A079-001E673976ED.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/A6DCB615-9A99-E411-B5F2-0025B3E063EA.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/AC40C7F5-9499-E411-8841-001E673986B0.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/AE7A3AD4-A799-E411-8D5B-001E67396D51.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/B0CE2BF2-A699-E411-BE79-001E67397B25.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/B230A801-AD99-E411-962C-002590FC5AC8.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/B6D04435-9D99-E411-91FB-002590A50046.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/BA32B780-9799-E411-933A-002590A831DC.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/C82A0E3A-9F99-E411-8675-002590200834.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/D8807F6E-A299-E411-8357-002590A8882A.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/DEAD7674-A499-E411-8700-002590200AC0.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/DEBB3EC0-9699-E411-9795-002590A3C95E.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/E047F315-A499-E411-95BB-002590A371AC.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/E4320E5F-9C99-E411-A2CE-0025B3E05D5C.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/E89A353D-9999-E411-9952-0025B3E0639C.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/F0EE9B2B-9899-E411-8CC3-002590200934.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/F8BFEA7A-9999-E411-99B6-002590A80DEA.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/00000/FE68ED3F-A599-E411-95B1-001E67396DCE.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/00F38639-9F99-E411-AD88-002481E15008.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/02438FF4-9899-E411-B201-0025B3E05BB8.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/0803AFE6-A299-E411-8D4F-002481E14F86.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/08055239-A199-E411-95E9-001E67397021.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/0A4C2E1C-9E99-E411-86F2-001E673975F8.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/16719620-9C99-E411-9E55-002590200AC0.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/18253F8E-B699-E411-983F-002590A831B6.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/1ADF26F2-9A99-E411-874F-002481E14F38.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/2EE164A4-8F99-E411-92E8-002481E14FB0.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/321DADC8-9799-E411-B098-001E67397215.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/3A05EAFA-AB99-E411-9BC7-002590200A58.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/7A637208-AF99-E411-9B72-0025B3E06612.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/92AF435F-A099-E411-9F6C-001E67397238.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/92EE4F22-9299-E411-97DD-001E673974EA.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/94128FB2-9C99-E411-89DD-002590A831CC.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/A218241B-9A99-E411-99A4-001E67397CAB.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/A8D0198C-9399-E411-B58C-001E67396568.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/B0B5AF73-9799-E411-88C0-002481E14F38.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/B4C28AFD-9499-E411-8960-001E67397238.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/B61C6184-9599-E411-ADE6-001E6739692D.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/D272980F-9399-E411-950E-002590A36FA2.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/F22D22C4-A699-E411-9377-001E67396568.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/F291A53A-9999-E411-9263-001E673972E2.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/F643A854-9E99-E411-A1D7-0025902008A8.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/F8E824DC-AC99-E411-AD46-001E6739815B.root',
'root://cms-xrd-global.cern.ch//store/mc/Phys14DR/DYToEE_M-50_Tune4C_13TeV-pythia8/GEN-SIM-RAW/PU40bx25_tsg_castor_PHYS14_25_V1-v2/10000/FED389C7-9D99-E411-8FCA-001E673970C1.root'
])

# output
f=ROOT.TFile("studyee/studyee.root","recreate")


# book histograms here
hGenElePt = ROOT.TH1F("hGenElePt","hGenElePt final",100,0,100) 
hGenMee = ROOT.TH1F("hGenMee","hGenMee final",150,0,150)
#hGenMeeeta = ROOT.TH1F("hGenMeeeta","hGenMeeeta",150,0,150) 
#hGenfinaltrackpt = ROOT.TH1F("hGenfinaltrackpt","hGenfinaltrackpt",100,0,100)
#Trackedele_eta =ROOT.TH1F("Trackedele_eta","Trackedele_eta",50,-3,3)
#Trackedele_pt27 =ROOT.TH1F("Trackedele_pt27","Trackedele_pt27",50,-3,3)
hGenMeeBeforeDecay = ROOT.TH1F("hGenMeeBeforeDecay","hGenMeeBeforeDecay initial",150,0,150) 
hGenMZ = ROOT.TH1F("hGenMZ","hGenMZ",150,0,150)

TrInielept = ROOT.TH1F("TrInielept","Initial Tracked ele pt",100,0,100)
TrInielept.GetXaxis().SetTitle("pT") 
TrInieleetabef = ROOT.TH1F("TrInieleetabef","Initial Tracked ele eta before pt>27 cut",60,-3,3)
TrInieleetabef.GetXaxis().SetTitle("#eta")
TrInieleetaaft = ROOT.TH1F("TrInieleetaaft","Initial Tracked ele eta after pt>27 cut",60,-3,3)
TrInieleetaaft.GetXaxis().SetTitle("#eta")
TrInileseleptbef = ROOT.TH1F("TrInileseleptbef","Initial Trackless ele pT without tracked pt>27 cut", 100, 0, 100)
TrInileseleptbef.GetXaxis().SetTitle("pT")
TrInileseleptaft = ROOT.TH1F("TrInileseleptaft","Initial Trackless ele pT with tracked pt>27 cut", 100, 0, 100)
TrInileseleptaft.GetXaxis().SetTitle("pT")
TrInileseleeta = ROOT.TH1F("TrInileseleeta","Initial Trackless ele eta",60,-3,3)
TrInileseleeta.GetXaxis().SetTitle("#eta")

Trelept = ROOT.TH1F("Trelept","Final Tracked ele pt",100,0,100)
Trelept.GetXaxis().SetTitle("pT") 
Treleetabef = ROOT.TH1F("Treleetabef","Final Tracked ele eta before pt>27 cut",60,-3,3)
Treleetabef.GetXaxis().SetTitle("#eta")
Treleetaaft = ROOT.TH1F("Treleetaaft","Final Tracked ele eta after pt>27 cut",60,-3,3)
Treleetaaft.GetXaxis().SetTitle("#eta")
Trleseleptbef = ROOT.TH1F("Trleseleptbef","Final Trackless ele pT without tracked pt>27 cut", 100, 0, 100)
Trleseleptbef.GetXaxis().SetTitle("pT")
Trleseleptaft = ROOT.TH1F("Trleseleptaft","Final Trackless ele pT with tracked pt>27 cut", 100, 0, 100)
Trleseleptaft.GetXaxis().SetTitle("pT")
Trleseleeta = ROOT.TH1F("Trleseleeta","Final Trackless ele eta",60,-3,3)
Trleseleeta.GetXaxis().SetTitle("#eta")

hGenElePt.Sumw2()
hGenMee.Sumw2()
hGenMeeBeforeDecay.Sumw2()
hGenMZ.Sumw2()

# print details?
debug = -1
# max N events to process?
nmax = -1

N=0.0
NZee=0.0
Ninieta=0.0
Ninimass=0.0
Ninitrpt=0.0
Ninitrlesspt=0.0
Nfinaleta=0.0
Nfinalmass=0.0
Ntrpt=0.0
Ntrlesspt=0.0

for event in events:

    #event counts:
    N=N+1.0

    # get genParticles
    event.getByLabel('genParticles','','HLT', genParticles)
    genParts = genParticles.product()

    # loop over all genParticles to find the Z boson
    for part in genParts:
        if abs(part.pdgId())==23 and part.status()==62 :
            genZ = part

    # get the two daughters of the Z boson
    genLepton1 = genZ.daughter(0)
    genLepton2 = genZ.daughter(1)

    # check if the two daughters are electrons, if not, go to the next event
    if abs(genLepton1.pdgId())!=11 or abs(genLepton2.pdgId())!=11 : continue
    NZee=NZee+1.0    
    # print the gen particle dacay tree starting from the Z boson
    if debug>1 :
        print "Analyze ",N," event:"
        print "GenZ: ndaughters=",genZ.numberOfDaughters(),"; status=",genZ.status()
        print "Dau1: pdg=",genLepton1.pdgId(),"; status=",genLepton1.status(),"; ndau=",genLepton1.numberOfDaughters(),"; pt=",genLepton1.pt()
        if genLepton1.numberOfDaughters()>0: printDauenghter(genLepton1, "++")
        print "Dau2: pdg=",genLepton2.pdgId(),"; status=",genLepton2.status(),"; ndau=",genLepton2.numberOfDaughters(),"; pt=",genLepton2.pt()
        if genLepton2.numberOfDaughters()>0: printDaughter(genLepton2, "++")


    # fill some histograms
    hGenMZ.Fill(genZ.mass())
    hGenMeeBeforeDecay.Fill((genLepton1.p4()+genLepton2.p4()).M())
    
    #--------------------------------for inital ee----------------------------
    # make eta cut and set tracked and trackless Ele
    if abs(genLepton1.eta())<2.5 and abs(genLepton2.eta())>2.5 and abs(genLepton2.eta())<3.0:
        TrIniEle = genLepton1
        TrInilessEle = genLepton2
        Ninieta=Ninieta+1.0
    elif abs(genLepton2.eta())<2.5 and abs(genLepton1.eta())>2.5 and abs(genLepton1.eta())<3.0:
        TrIniEle = genLepton2
        TrInilessEle = genLepton1
        Ninieta=Ninieta+1.0
    # if the event don't pass the eta cut, go to next event
    else: continue 
          
    # make mass cut for ele pass eta cut
    if (TrIniEle.p4()+TrInilessEle.p4()).M()>60 and  (TrIniEle.p4()+TrInilessEle.p4()).M()<120:
        Ninimass=Ninimass+1.0
        TrInielept.Fill(TrIniEle.pt())
        TrInieleetabef.Fill(TrIniEle.eta()) 
        TrInileseleptbef.Fill(TrInilessEle.pt())
        TrInileseleeta.Fill(TrInilessEle.eta())
   # make pt cut for tracked
        if TrIniEle.pt()>27.0:
           Ninitrpt=Ninitrpt+1.0
           TrInieleetaaft.Fill(TrIniEle.eta())
           TrInileseleptaft.Fill(TrInilessEle.pt())
    # make pt cut for trackless
           if TrInilessEle.pt()>15.0:
              Ninitrlesspt=Ninitrlesspt+1.0



    #----------------------------------for final ee------------------------------------------------------------    
    # get the final daughter electrons with generator status to be 1
    genEle1 = genLepton1
    if genLepton1.numberOfDaughters()>0: genEle1 = getStatusOneDaughter(genLepton1,11)
    genEle2 = genLepton2
    if genLepton2.numberOfDaughters()>0: genEle2 = getStatusOneDaughter(genLepton2,11)

    # make eta cut and set tracked and trackless Ele
    if abs(genEle1.eta())<2.5 and abs(genEle2.eta())>2.5 and abs(genEle2.eta())<3.0:
        TrEle = genEle1
        TrlessEle = genEle2
        Nfinaleta=Nfinaleta+1.0
    elif abs(genEle2.eta())<2.5 and abs(genEle1.eta())>2.5 and abs(genEle1.eta())<3.0:
        TrEle = genEle2
        TrlessEle = genEle1
        Nfinaleta=Nfinaleta+1.0
    # if the event don't pass the eta cut, go to next event
    else: continue           

    # make mass cut for ele pass eta cut
    if (TrEle.p4()+TrlessEle.p4()).M()>60 and  (TrEle.p4()+TrlessEle.p4()).M()<120:
        Nfinalmass=Nfinalmass+1.0
        Trelept.Fill(TrEle.pt())
        Treleetabef.Fill(TrEle.eta()) 
        Trleseleptbef.Fill(TrlessEle.pt())
        Trleseleeta.Fill(TrlessEle.eta())
   # make pt cut for tracked
        if TrEle.pt()>27.0:
           Ntrpt=Ntrpt+1.0
           Treleetaaft.Fill(TrEle.eta())
           Trleseleptaft.Fill(TrlessEle.pt())
    # make pt cut for trackless
           if TrlessEle.pt()>15.0:
              Ntrlesspt=Ntrlesspt+1.0
       



    # print the final selected 2 status=1 electrons
    if debug>0:
        print "GenEle1: pdg=",genEle1.pdgId(),"; status=",genEle1.status(),"; ndau=",genEle1.numberOfDaughters(),"; pt=",genEle1.pt()
        print "GenEle2: pdg=",genEle2.pdgId(),"; status=",genEle2.status(),"; ndau=",genEle2.numberOfDaughters(),"; pt=",genEle2.pt()


    #fill the histograms:
    hGenElePt.Fill(genEle1.pt())
    hGenElePt.Fill(genEle2.pt())
    hGenMee.Fill((genEle1.p4()+genEle2.p4()).M())

    # break after some events
    if nmax!=-1 and N>nmax: break

# write output
#print "N=",N,"; NZee=",NZee,";Nfinaletal=",Nfinaletal,";Nfinalmassl=",Nfinalmassl
print "-----------------------------------------------------------------------"
print "Total # of Events: N=",N
print "# of Events with two eles of mother Z: NZee=",NZee,"     ---eff=",NZee/N
#print "--initial ee daughter of Zee event pass the eta cut: Neta=",Neta,"    ---eff=",Neta/NZee
#print "-----initial ee daughter of Zee event pass the mass cut: Nmass=",Nmass,"   ---eff=",Nmass/Neta
print "--------------------------Initial ee daugter---------------------------"
print "Initial ee daughter of Zee event pass the eta cut: Ninieta=", Ninieta,"   ---eff=",Ninieta/NZee
print "--Initial ee daughter of Zee pass the mass cut: Ninimass=",Ninimass,"   ---eff=",Ninimass/Ninieta
print "----tracked ele pass pt>27 cut: Ninitrpt=",Ninitrpt,"   ---eff=",Ninitrpt/Ninimass
print "--------trackless ele pass pt>15 cut: Ninitrlesspt=",Ninitrlesspt,"   ---eff=",Ninitrlesspt/Ninitrpt
print "------------Initial gen eff=",Ninitrlesspt/NZee
print "---------------------------Final ee daugter--------------------------"
print "final ee daughter of Zee event pass the eta cut: Nfinaleta=", Nfinaleta,"   ---eff=",Nfinaleta/NZee
print "--final ee daughter of Zee pass the mass cut: Nfinalmass=",Nfinalmass,"   ---eff=",Nfinalmass/Nfinaleta
print "----tracked ele pass pt>27 cut: Ntrpt=",Ntrpt,"   ---eff=",Ntrpt/Nfinalmass
print "--------trackless ele pass pt>15 cut: Ntrlesspt=",Ntrlesspt,"   ---eff=",Ntrlesspt/Ntrpt
print "------------final gen eff=",Ntrlesspt/NZee


f.cd()
hGenElePt.Write()
hGenMee.Write()
hGenMeeBeforeDecay.Write()
hGenMZ.Write()
TrInielept.Write()
TrInieleetabef.Write()
TrInieleetaaft.Write()
TrInileseleptbef.Write()
TrInileseleptaft.Write()
TrInileseleeta.Write()

Trelept.Write()
Treleetabef.Write()
Treleetaaft.Write()
Trleseleptbef.Write()
Trleseleptaft.Write()
Trleseleeta.Write()



c = ROOT.TCanvas("c","Plots",800,800)
c.cd()
TrInielept.Draw()
TrInielept.SetFillColor(41)
c.Print("studyee/Ini_tracked_pt.pdf","pdf")

c.Clear()
TrInieleetabef.Draw()
TrInieleetabef.SetFillColor(41)
TrInieleetabef.SetTitle("Tracked electron before and after pt>27 cut; #eta; Event")
TrInieleetaaft.SetLineWidth(3)
TrInieleetaaft.SetLineColor(2)
TrInieleetaaft.Draw("same")
leg = ROOT.TLegend(0.76,0.78,0.97,0.92)
leg.AddEntry(TrInieleetabef,"before pt>27 cut","f")
leg.AddEntry(TrInieleetaaft,"after pt>27 cut","l")
leg.Draw()
c.Print("studyee/Ini_trackedeta_befaft_pt27cut.pdf","pdf")

c.Clear()
TrInileseleptbef.Draw()
TrInileseleptbef.SetFillColor(41)
TrInileseleptbef.SetTitle("Trackless electron before and after tracked pt>27 cut; pT; Event")
TrInileseleptaft.SetLineWidth(3)
TrInileseleptaft.SetLineColor(2)
TrInileseleptaft.Draw("same")
leg.Draw()
c.Print("studyee/Ini_tracklessPT-befaft_trackedpt27cut.pdf","pdf")

c.Clear()
TrInileseleeta.Draw()
TrInileseleeta.SetFillColor(41)
c.Print("studyee/Ini_trackless_eta.pdf","pdf")

c.Clear()
Trelept.Draw()
Trelept.SetFillColor(41)
c.Print("studyee/Final_tracked_pt.pdf","pdf")

c.Clear()
Treleetabef.Draw()
Treleetabef.SetFillColor(41)
Treleetabef.SetTitle("Tracked electron before and after pt>27 cut; #eta; Event")
Treleetaaft.SetLineWidth(3)
Treleetaaft.SetLineColor(2)
Treleetaaft.Draw("same")
leg.Draw()
c.Print("studyee/Final_trackedeta_befaft_pt27cut.pdf","pdf")

c.Clear()
Trleseleptbef.Draw()
Trleseleptbef.SetFillColor(41)
Trleseleptbef.SetTitle("Trackless electron before and after tracked pt>27 cut; pT; Event")
Trleseleptaft.SetLineWidth(3)
Trleseleptaft.SetLineColor(2)
Trleseleptaft.Draw("same")
leg.Draw()
c.Print("studyee/Final_tracklessPT-befaft_trackedpt27cut.pdf","pdf")

c.Clear()
Trleseleeta.Draw()
Trleseleeta.SetFillColor(41)
c.Print("studyee/Final_trackless_eta.pdf","pdf")




f.Close()


 
    # if (abs(genEle1.eta())<2.5 and abs(genEle2.eta())>2.5 and abs(genEle2.eta())<3.0):
    #    if (genEle1.p4()+genEle2.p4()).M()>60.0 and (genEle1.p4()+genEle2.p4()).M()<120.0:
    #        Nfinalmass=Nfinalmass+1.0
    #        hGenfinaltrackpt.Fill(genEle1.pt())
    #        Trackedele_eta.Fill(genEle1.eta())
    #        if genEle1.pt()>27.0:
    #           Trackedele_pt27.Fill(genEle1.eta())
    #if (abs(genEle2.eta())<2.5 and abs(genEle1.eta())>2.5 and abs(genEle1.eta())<3.0):
    #    if (genEle1.p4()+genEle2.p4()).M()>60.0 and (genEle1.p4()+genEle2.p4()).M()<120.0:
    #      Nfinalmass=Nfinalmass+1.0
    #        hGenfinaltrackpt.Fill(genEle2.pt())
    #        Trackedele_eta.Fill(genEle2.eta())
    #        if genEle2.pt()>27.0:
    #           Trackedele_pt27.Fill(genEle2.eta())   
        
