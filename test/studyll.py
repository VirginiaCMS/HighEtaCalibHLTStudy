#!/bin/python

# Initial example scripts for HighEta HLT studies
# Contact: Hengne.Li@cern.ch 
# 11 Aug. 2015
# modified to match the DYLL sample which was shown in the ppt.
# modified to cut both the inital and final ee daughters .   Aug21.2015
# Add all the DYLL files, run get all plots and root file. Aug24.2015
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
events = Events(['root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/047993F0-27F5-E411-A55F-0025B3E05DAC.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/127E44D8-A4F4-E411-BB3A-00259073E410.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/141A559D-12F5-E411-B99F-6CC2173BC370.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/228AA79B-3AF4-E411-9CC6-20CF3027A5AE.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/28972936-BFF4-E411-9817-0025907B4EEC.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/44C673DF-25F5-E411-935E-00266CF2507C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/462EF5EE-25F5-E411-A1EB-00266CF9B254.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/4EEF9968-3AF4-E411-A65F-002590D0B032.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/527F2517-21F4-E411-9822-0025907277E8.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/5421FA4A-28F5-E411-9BB7-001E67396644.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/5C185288-3AF4-E411-9090-20CF305B04CC.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/6470412E-45F4-E411-BD03-20CF305B0585.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/6AD1B49F-1BF5-E411-964E-0025905C4300.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/70A1B28F-3AF4-E411-819B-00259073E406.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/76A24318-28F5-E411-A2D3-001E67398D5E.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/92FF04E5-25F5-E411-BDD0-008CFA002634.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/A25FC3A6-9FF4-E411-8C92-5254003312EA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/AC716D03-3BF5-E411-971F-0025905C95FA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/AEEA6424-A8F4-E411-9332-485B39800B97.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/B61535EC-B4F4-E411-9E3D-BCAEC54B3067.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/DAFD2A3E-9DF4-E411-9D2E-00259073E3A2.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/00000/F85A235B-39F5-E411-9130-00266CF32FA0.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/0005BDF7-29F4-E411-A5AA-525400245E18.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/0077A47D-13F4-E411-8800-20CF3056171D.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/024F3F76-1EF4-E411-868F-0025905A60B6.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/0671475F-61F4-E411-8978-0025904C6374.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/067A6E51-58F4-E411-B2C1-001E67397391.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/0899D755-2EF4-E411-9231-E0CB4E19F9B8.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/08E0F48F-2BF4-E411-BA08-0025905A6094.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/0A1C10DC-2BF4-E411-8839-485B39800C1D.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/0AA12C0D-13F4-E411-B918-E0CB4E29C4D0.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/0AD15009-54F4-E411-AB4C-3417EBE64CDB.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/0C90BB8C-1DF4-E411-9859-0025905B858A.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/0CAAA3E5-2BF4-E411-8FF9-20CF3027A62F.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/0E80BFFC-16F4-E411-843D-52540006FB8D.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/100F388E-2BF4-E411-A9D0-00259073E3CE.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/10F09DB5-53F4-E411-A771-008CFA000BB8.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/12B97AFD-0EF4-E411-A10E-525400C0AB82.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/12F50553-2EF4-E411-80F2-525400872AA7.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/141E6051-2DF4-E411-B2AA-00259073E3FA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/14A0CE45-84F4-E411-AA1A-00259073E3D6.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/1619A278-12F4-E411-AAF4-0025907B4F50.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/18116BC0-16F4-E411-B9DA-20CF3027A5B5.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/182C44D7-1AF4-E411-A2A3-5254009A38FA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/183C895E-61F4-E411-BF93-0025905C3DD0.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/1A2970B1-60F4-E411-82E7-0025904CF712.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/1A298058-13F4-E411-92F8-E0CB4E29C4F7.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/1AD8ABDF-60F4-E411-BC83-0025905C3D96.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/22119255-2DF4-E411-9F03-00259073E4B6.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/244841D9-06F5-E411-973E-002590593920.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/245E267A-3DF5-E411-84C8-00A0D1EE8AF0.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/24A82140-15F4-E411-B536-0025907B501C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/26199765-57F4-E411-8F21-001E67396D10.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/26FA42F1-57F4-E411-A5A4-0025B3E05C7E.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/283A26C3-29F4-E411-9EF7-0025905A60A6.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/28B85968-19F4-E411-8137-20CF305B052F.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/28DF5B63-2CF4-E411-9AA7-20CF3027A5B5.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/28E8CC8E-18F4-E411-91E6-485B39800B8B.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/2A4D6315-17F4-E411-9BEB-525400929F2C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/2C1F8488-59F4-E411-882F-C4346BBCD528.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/324904A2-53F4-E411-86A8-00A0D1EC3950.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/32789E5C-61F4-E411-AECC-0025904C637E.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/34DD131A-59F4-E411-B984-002590A8882C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/362A8155-57F4-E411-8790-001E67396D10.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/3633318A-28F4-E411-9949-00259073E502.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/366F5B46-15F4-E411-8497-002590D0B03A.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/38172C44-60F4-E411-86D2-0025905C4300.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/38974C86-28F4-E411-8053-00259073E53C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/38F7EEE5-57F4-E411-A015-002590200878.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/3A44CD50-60F4-E411-A1B7-0025904C678A.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/3A6B8F45-78F4-E411-BD80-E0CB4EA0A909.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/3A9C154D-2DF4-E411-AA38-52540006FDD6.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/3A9D2E04-2AF4-E411-AF83-E0CB4E29C4F6.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/3C2CBCED-6CF4-E411-A1EF-20CF3027A5D1.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/3CCEF46C-2CF4-E411-A9BE-485B3989725B.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/3E01E7EA-13F4-E411-B664-BCAEC50971D8.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/4213BB56-59F4-E411-88D8-6CC2173AB870.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/423217AA-53F4-E411-B684-00266CFAE050.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/4245E0EA-13F4-E411-B5F5-20CF3027A5F3.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/447F1A45-57F4-E411-940A-D8D385FF4A72.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/460F5117-58F4-E411-B174-001E673974EA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/46559250-2EF4-E411-B58C-E0CB4E1A1163.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/4677A3F4-56F4-E411-83A6-001E67398BE7.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/4EC182EB-29F4-E411-B23E-00259073E514.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/505BC3D0-2BF4-E411-8225-0025907B4F14.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/5086AD0B-54F4-E411-9B3F-3417EBE64483.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/52A2FE8E-11F4-E411-B1AD-E0CB4E29C4C6.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/52DC46A1-18F4-E411-A67B-525400245E18.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/547A3FD2-2BF4-E411-A389-00259073E3FA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/54E92666-19F4-E411-A549-E0CB4E29C51D.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/568909C1-20F4-E411-9756-0025905A60D2.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/5867F609-46F5-E411-83DD-0025904C5DDA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/587B1768-2CF4-E411-A765-00259073E3A2.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/5895BCA4-94F4-E411-9308-003048F0E59C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/58AC140F-57F4-E411-B1AC-002590200894.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/58D1804E-59F4-E411-9641-6CC2173BBE60.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/5A3CB085-2BF4-E411-9ADC-00259073E4E2.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/5A8C4A22-0EF4-E411-9CFC-525400C0AB82.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/5C80BC52-57F4-E411-9BE6-0025B3E05DCA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/5C92F54F-2DF4-E411-AAFB-0025907B4F60.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/5CFF3DA3-DDF4-E411-87E7-0025904C650A.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/5EB49007-2AF4-E411-963B-00259073E4C2.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/5EF1D7C2-2BF4-E411-9687-5254000902E4.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/6244F82D-4DF5-E411-B307-002590DB91CA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/628C5AA1-53F4-E411-88FA-00266CFAE8C4.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/66239ED1-2BF4-E411-94A9-E0CB4E29C512.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/66C6B85D-2DF4-E411-AC68-002590596486.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/6854A3AB-14F4-E411-AC54-BCAEC54B303A.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/6894AA5E-2EF4-E411-A616-00259073E390.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/6AA44FF1-57F4-E411-A78A-001E67396892.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/6AA6A64D-57F4-E411-B75C-D8D385FF4A7C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/6ABE82B1-18F4-E411-96C1-0025905B859E.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/6AD13D09-61F4-E411-A5F5-0025905C3E68.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/6C403D4E-2EF4-E411-96CD-00259073E3F2.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/6C72395E-2CF4-E411-9391-E0CB4E29C4F7.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/6E74CEE3-17F4-E411-82C3-525400929F2C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/722A43E1-13F4-E411-9D2A-0025907B4F1C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/7236874D-57F4-E411-B059-002590200810.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/72DD2CE7-57F4-E411-BA19-0025B3E05D74.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/74373B5A-57F4-E411-88B7-001E67396BB7.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/762E0F13-54F4-E411-AFB9-7845C4FC370D.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/76790953-2EF4-E411-A8B7-002590D0B092.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/768AD601-1AF4-E411-AFC1-485B39800BD5.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/769342FF-60F4-E411-985D-0025905C3D6C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/76D8C682-64F4-E411-905B-AC162DACC328.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/7817F470-12F4-E411-A195-0025907B4FCA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/781876AF-14F4-E411-BA32-002590D0B06C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/78986A58-1AF4-E411-BF9F-00259073E34E.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/78BE3C50-EDF4-E411-862E-00A0D1EC3950.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/7AF9645E-61F4-E411-8785-0025905C42F4.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/7C3F8BD0-2BF4-E411-9F55-5254003312EA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/7CA7B251-61F4-E411-B9C7-0025905C4300.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/7CD07522-54F4-E411-A70F-7845C4FC3758.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/7E0C39CC-80F4-E411-A691-00259074AE8C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/7ECC2F3A-93F4-E411-9206-00266CF32684.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/86054C51-2EF4-E411-8045-00259073E3CE.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/88A2A4EA-29F4-E411-AAEC-525400E604B7.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/88C7CE54-11F4-E411-83B7-0025907B4FCA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/8C50A726-57F4-E411-BE84-001E67396BA3.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/8CABE684-2CF4-E411-B81C-0025905A6064.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/8CF24309-54F4-E411-8031-848F69FD2925.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/8E26C289-1AF4-E411-A2E2-20CF305B052F.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/8E82A8BF-29F4-E411-A806-0025905A6094.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/8E8568AA-53F4-E411-8435-00266CFAE2F0.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/90B8D5DC-15F4-E411-A3D2-002590D0B06C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/90BE179F-60F4-E411-B5CA-0025904B7C26.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/90C57E8A-F2F4-E411-A82A-008CFA0518D4.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/9266FFF8-56F4-E411-9380-002481E14E56.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/9284E852-2DF4-E411-BF3D-002590D0B092.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/92A37D67-0FF4-E411-AE8C-E0CB4E19F962.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/94C892F1-16F4-E411-9E0D-525400E604B7.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/967BD167-61F4-E411-9477-0025904C6416.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/9A2C1755-2EF4-E411-85A9-525400245E18.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/9A86A803-17F4-E411-ABE7-525400929F2C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/9AE400D4-2BF4-E411-8D60-00259074AE5C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/9CF17CB8-57F4-E411-A974-0025B3E05D0A.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/9E2F5B96-60F4-E411-9877-0025905C3D98.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/A2B11546-61F4-E411-987A-0025905C9742.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/A2E25086-28F4-E411-9E3C-00259074AE8C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/A4DEF0F5-60F4-E411-B32B-0025904C51F0.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/A600622C-18F4-E411-A3B3-525400245E18.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/A656698A-3DF5-E411-842F-1CC1DE050110.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/A65D130D-23F5-E411-BF24-002590FC5AD0.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/A66A0677-1EF4-E411-9BBE-0025905B8598.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/A66DFFFB-56F4-E411-8A66-0025B3E05D74.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/AAF63FCF-15F4-E411-A724-525400778469.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/ACA6FA2A-11F4-E411-A7AA-E0CB4E553642.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/ACF39667-2CF4-E411-8F34-00259073E452.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/ACF61444-60F4-E411-8121-0025905C9742.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/B2836AB4-57F4-E411-88D9-0025B3E05CAA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/B488CA79-12F4-E411-8CA2-E0CB4E553642.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/B6E247E3-15F4-E411-914B-52540006FB8D.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/B8A94E5E-61F4-E411-8EE8-0025905C3DD0.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/BA3E0222-12F4-E411-8D77-E0CB4E29C4F7.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/BA948CD4-83F4-E411-BC4B-0025901D4C46.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/BAA5D3D4-2BF4-E411-927A-E0CB4E553677.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/BE1A275A-61F4-E411-BBD7-0025905C4264.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/BED0E6A1-53F4-E411-B856-00266CF279F8.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/BEE11195-60F4-E411-BD9A-0025904C656A.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/C0D839AF-61F4-E411-810C-0025905C3DF8.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/C25C9B92-28F4-E411-8E8D-00259073E36E.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/C270193C-60F4-E411-A567-0025905C2CD0.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/C62DBC88-28F4-E411-97A6-525400929F2C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/C64A6752-2DF4-E411-8031-00259073E438.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/C6B864CF-2BF4-E411-8FF8-00259073E438.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/C6C5D740-58F4-E411-A21B-002590A80DEA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/C8EF1456-57F4-E411-8D6D-001E67396BB7.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/CA52A7C1-2BF4-E411-9069-5254000902E4.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/CA5832FB-29F4-E411-8D96-00259073E3CE.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/CADD8655-2DF4-E411-B69C-00259073E364.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/CC19C7E3-1FF5-E411-8CD0-848F69FD2484.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/CC1BF1FE-29F4-E411-A310-52540023C679.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/CC96A126-18F4-E411-B027-52540006FB8D.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/CE818A28-54F4-E411-9870-848F69FD2997.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/CEB267B2-61F4-E411-8B65-0025905C96A6.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/CEEBA16A-2CF4-E411-B154-BCAEC50971D0.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/D02949D8-03F5-E411-95A7-0025905C2C84.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/D093DC5D-2CF4-E411-BAD1-E0CB4E19F9A5.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/D09EA3F7-60F4-E411-A528-0025905C3E38.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/D26654C2-57F4-E411-9CA5-001E673987D2.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/D2E080D7-0FF4-E411-A1D7-002590D0AFE4.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/D43D54A4-60F4-E411-8FF3-0025904C51F0.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/D6DEE6EB-29F4-E411-AB95-00259073E3CE.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/D821E05D-2EF4-E411-8B54-E0CB4E4408EF.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/D8274260-2DF4-E411-A845-F46D043B4216.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/D8B65243-32F4-E411-BF41-0025905A608A.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/D8DEAC8B-2BF4-E411-B96C-52540049CF9E.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/DA2C4DED-60F4-E411-B89C-0025905C42F2.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/DACA18AD-14F4-E411-BD06-20CF305B052D.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/DC89E499-81F4-E411-9B00-E0CB4E19F9BB.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/DE964984-14F4-E411-8F1C-20CF3056171D.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/E2408366-2CF4-E411-B676-485B39897259.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/E454E16A-2CF4-E411-819E-00259073E442.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/E466B6F8-57F4-E411-840B-002590200B00.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/E4759257-59F4-E411-B28E-6CC2173BBA60.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/E601E807-57F4-E411-A6BD-002481E153FA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/E68CA005-61F4-E411-BB45-0025905C2CD0.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/E6954F64-13F4-E411-B3DF-BCAEC54B303A.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/E8F4727A-14F4-E411-A4EC-5254001351DD.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/E8F48335-61F4-E411-A020-0025905C4264.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/EA09C43D-10F5-E411-ABFA-00259073E53C.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/ECF48AA1-53F4-E411-9195-00266CFAE268.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/EE1594A7-53F4-E411-BE3B-00266CF9B254.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/EE1F6201-54F4-E411-BA6D-7845C4FC3A16.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/F0D92718-61F4-E411-B471-0025905C96EA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/F2011AD9-15F4-E411-BE92-525400E604B7.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/F2C648A9-60F4-E411-9092-0025905C3DF8.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/F2CD6D97-28F4-E411-BEC3-002590D0AFFC.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/F4D35CFE-29F4-E411-B73B-0025907B5038.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/F4D523CF-2BF4-E411-95CC-002590D0B0BA.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/F4FA4174-16F4-E411-9625-525400F35832.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/F82B2CEB-57F4-E411-82DE-002590147CA2.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/FAE501EC-60F4-E411-8153-0025904C6378.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/FCB918FD-12F4-E411-8F22-0025907B4EF2.root',
'root://cms-xrd-global.cern.ch//store/mc/RunIISpring15Digi74/DYToLL_M_1_TuneCUETP8M1_13TeV_pythia8/GEN-SIM-RAW/AVE_40_BX_25ns_tsg_MCRUN2_74_V7-v2/50000/FEE2884B-60F4-E411-9258-0025905C4264.root'
])
# output
f=ROOT.TFile("studyll/studyll.root","recreate")


# book histograms here
hGenElePt = ROOT.TH1F("hGenElePt","hGenElePt final",100,0,100) 
hGenMee = ROOT.TH1F("hGenMee","hGenMee final",150,0,150)
#hGenMeeeta = ROOT.TH1F("hGenMeeeta","hGenMeeeta",150,0,150) 
#hGenfinaltrackpt = ROOT.TH1F("hGenfinaltrackpt","hGenfinaltrackpt",100,0,100)
#Trackedele_eta =ROOT.TH1F("Trackedele_eta","Trackedele_eta",50,-3,3)
#Trackedele_pt27 =ROOT.TH1F("Trackedele_pt27","Trackedele_pt27",50,-3,3)
hGenMeeBeforeDecay = ROOT.TH1F("hGenMeeBeforeDecay","hGenMeeBeforeDecay initial",150,0,150) 
hGenMZ = ROOT.TH1F("hGenMZ","hGenMZ after MZ>50 cut",150,0,150)
hGenZmass = ROOT.TH1F("hGenZmass","hGenZmass before 50 cut",150,0,150)

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
TrInileseleeta = ROOT.TH1F("TrInileseleeta","Initial Tracked ele eta",60,-3,3)
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
Trleseleeta = ROOT.TH1F("Trleseleeta","Final Tracked ele eta",60,-3,3)
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
NZ=0.0
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
        
            hGenZmass.Fill(genZ.mass())            

    if genZ.mass()<50 : continue
    # get the two daughters of the Z boson
    genLepton1 = genZ.daughter(0)
    genLepton2 = genZ.daughter(1)
    #number of Z after mass>50 cut
    NZ=NZ+1.0                        

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
print "# of Z pass the mass>50 cut: NZ=",NZ,"    ---eff=",NZ/N
print "# of Events with two eles of mother Z: NZee=",NZee,"     ---eff=",NZee/NZ
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
hGenZmass.Write()
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
c.Print("studyll/Ini_tracked_pt.pdf","pdf")

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
c.Print("studyll/Ini_trackedeta_befaft_pt27cut.pdf","pdf")

c.Clear()
TrInileseleptbef.Draw()
TrInileseleptbef.SetFillColor(41)
TrInileseleptbef.SetTitle("Trackless electron before and after tracked pt>27 cut; pT; Event")
TrInileseleptaft.SetLineWidth(3)
TrInileseleptaft.SetLineColor(2)
TrInileseleptaft.Draw("same")
leg.Draw()
c.Print("studyll/Ini_tracklessPT-befaft_trackedpt27cut.pdf","pdf")

c.Clear()
TrInileseleeta.Draw()
TrInileseleeta.SetFillColor(41)
c.Print("studyll/Ini_trackless_eta.pdf","pdf")

c.Clear()
Trelept.Draw()
Trelept.SetFillColor(41)
c.Print("studyll/Final_tracked_pt.pdf","pdf")

c.Clear()
Treleetabef.Draw()
Treleetabef.SetFillColor(41)
Treleetabef.SetTitle("Tracked electron before and after pt>27 cut; #eta; Event")
Treleetaaft.SetLineWidth(3)
Treleetaaft.SetLineColor(2)
Treleetaaft.Draw("same")
leg.Draw()
c.Print("studyll/Final_trackedeta_befaft_pt27cut.pdf","pdf")

c.Clear()
Trleseleptbef.Draw()
Trleseleptbef.SetFillColor(41)
Trleseleptbef.SetTitle("Trackless electron before and after tracked pt>27 cut; pT; Event")
Trleseleptaft.SetLineWidth(3)
Trleseleptaft.SetLineColor(2)
Trleseleptaft.Draw("same")
leg.Draw()
c.Print("studyll/Final_tracklessPT-befaft_trackedpt27cut.pdf","pdf")

c.Clear()
Trleseleeta.Draw()
Trleseleeta.SetFillColor(41)
c.Print("studyll/Final_trackless_eta.pdf","pdf")




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
        
