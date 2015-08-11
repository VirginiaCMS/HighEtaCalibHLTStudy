#!/bin/python

# Initial example scripts for HighEta HLT studies
# Contact: Hengne.Li@cern.ch 
# 11 Aug. 2015

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
events = Events([
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/047993F0-27F5-E411-A55F-0025B3E05DAC.root',
#'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/127E44D8-A4F4-E411-BB3A-00259073E410.root'
])

# output
f=ROOT.TFile("study.root","recreate")


# book histograms here
hGenElePt = ROOT.TH1F("hGenElePt","hGenElePt",100,0,100) 
hGenMee = ROOT.TH1F("hGenMee","hGenMee",150,0,150) 
hGenMeeBeforeDecay = ROOT.TH1F("hGenMeeBeforeDecay","hGenMeeBeforeDecay",150,0,150) 
hGenMZ = ROOT.TH1F("hGenMZ","hGenMZ",150,0,150)

hGenElePt.Sumw2()
hGenMee.Sumw2()
hGenMeeBeforeDecay.Sumw2()
hGenMZ.Sumw2()

# print details?
debug = 0

N=0.0
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

    # print the gen particle dacay tree starting from the Z boson
    if debug>1 :
        print "Analyze ",N," event:"
        print "GenZ: ndaughters=",genZ.numberOfDaughters(),"; status=",genZ.status()
        print "Dau1: pdg=",genLepton1.pdgId(),"; status=",genLepton1.status(),"; ndau=",genLepton1.numberOfDaughters(),"; pt=",genLepton1.pt()
        if genLepton1.numberOfDaughters()>0: printDaughter(genLepton1, "++")
        print "Dau2: pdg=",genLepton2.pdgId(),"; status=",genLepton2.status(),"; ndau=",genLepton2.numberOfDaughters(),"; pt=",genLepton2.pt()
        if genLepton2.numberOfDaughters()>0: printDaughter(genLepton2, "++")


    # fill some histograms
    hGenMZ.Fill(genZ.mass())
    hGenMeeBeforeDecay.Fill((genLepton1.p4()+genLepton2.p4()).M())

    # get the final daughter electrons with generator status to be 1
    genEle1 = genLepton1
    if genLepton1.numberOfDaughters()>0: genEle1 = getStatusOneDaughter(genLepton1,11)
    genEle2 = genLepton2
    if genLepton2.numberOfDaughters()>0: genEle2 = getStatusOneDaughter(genLepton2,11)

    # print the final selected 2 status=1 electrons
    if debug>0:
        print "GenEle1: pdg=",genEle1.pdgId(),"; status=",genEle1.status(),"; ndau=",genEle1.numberOfDaughters(),"; pt=",genEle1.pt()
        print "GenEle2: pdg=",genEle2.pdgId(),"; status=",genEle2.status(),"; ndau=",genEle2.numberOfDaughters(),"; pt=",genEle2.pt()


    #fill the histograms:
    hGenElePt.Fill(genEle1.pt())
    hGenElePt.Fill(genEle2.pt())
    hGenMee.Fill((genEle1.p4()+genEle2.p4()).M())

    # break after some events
    #if N>10: break

# write output
f.cd()
hGenElePt.Write()
hGenMee.Write()
hGenMeeBeforeDecay.Write()
hGenMZ.Write()
f.Close()


