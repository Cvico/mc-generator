""" This is the main analyzer """
from framework.particles import lepton_obj, jet_obj
import ROOT as r
import numpy as np
import os, sys
from copy import deepcopy

class baseAnalyzer(object):
    uncs = ["scale", "renorm", "combined"]
    def __init__(self, options, file_):
        # Save information in attributes
        self.inputFolder = options.inputFolder
        self.nEvents = options.nEvents
        self.outpath = options.outpath
        self.file = file_

        # Open rootfile and store trees
        self.fname = os.path.join(self.inputFolder, self.file)
        
        self.rfile = r.TFile.Open(self.fname)
        self.tree_events = self.rfile.Get("Events")
        self.tree_runs = self.rfile.Get("Runs")
        
        self.name = file_.replace(".root", "")
        # Create histograms
        self.createHistograms()
        return

    def loop(self):
        """ Here you have to implement your own analysis """
        return

    def createHistograms(self):
        """ Here you define what histograms are plotted """
        return

    def get_histograms(self): 
        return self.histograms

    def save_in_tree(self):
        outname = os.path.join(self.outpath, self.file.replace(".root", "_hists.root"))
        f = r.TFile.Open(outname, "RECREATE")
        for hname, h in self.histograms.items():
            h.Write(hname)  
        f.Close()
        return
    
    def get_histograms(self): 
        return self.histograms
    
    def progressBar(self, count_value, total, suffix=''):
        """ Just a silly progress bar to debug if the code is running """
        bar_length = 100
        filled_up_Length = int(round(bar_length* count_value / float(total)))
        percentage = round(100.0 * count_value/float(total),1)
        bar = '=' * filled_up_Length + '-' * (bar_length - filled_up_Length)
        sys.stdout.write('[%s] %s%s ...%s\r' %(bar, percentage, '%', suffix))
        sys.stdout.flush()
        return
    
    def createHistograms(self):
        """ Here you define what histograms are plotted """
        
        # These are some of the basic ones one can do with
        # nanogen information. 
        self.histograms = {} 

        # Lepton related variables 
        self.histograms["leadingLeptonPt"]   = r.TH1F(self.name + '_LeadingLeptonPt',   
                                                        r';1st lepton p_{T} (GeV);Events', 
                                                        10, 0, 300)
        self.histograms["leadingLeptonEta"]  = r.TH1F(self.name + '_LeadingLeptonEta',  
                                                        r';1st lepton #ETA;Events',
                                                        10 ,-3, 3)
        self.histograms["trailingLeptonPt"]  = r.TH1F(self.name + '_trailingLeptonPt',  
                                                        r';2nd p_{T} (GeV);Events', 
                                                        10, 0, 200)
        self.histograms["trailingLeptonEta"] = r.TH1F(self.name + '_trailingLeptonEta', 
                                                        r';2nd lepton #ETA;Events',
                                                        10 ,-3, 3)

        # Jet related variables 
        self.histograms["Njet"]           = r.TH1F(self.name + '_Njet',
                                                    r';Njets; Events',
                                                    5, 2, 7)
        self.histograms["leadingJetPt"]   = r.TH1F(self.name + '_LeadingJetPt',
                                                    r';1st jet p_{T} (GeV);Events',
                                                    10, 0, 300)
        self.histograms["leadingJetEta"]  = r.TH1F(self.name + '_LeadingJetEta',
                                                    r';1st jet #ETA;Events',
                                                    10 ,-3, 3)
        self.histograms["trailingJetPt"]  = r.TH1F(self.name + '_trailingJetPt',
                                                    r';2nd jet p_{T}^{j} (GeV);Events',
                                                    10, 0, 200)
        self.histograms["trailingJetEta"] = r.TH1F(self.name + '_trailingJetEta',
                                                    r';2nd jet #ETA;Events',
                                                    10 ,-3, 3)
        
        # Make a copy of the histograms for variations
        vardict = {}
        for unc in self.uncs:
            for uncdir in ["up", "down"]:
                for hname, h in self.histograms.items():
                    label = "_%s_%s"%(unc, uncdir)
                    newname = h.GetName() + label
                    hvar = deepcopy(h.Clone(newname))
                    vardict[hname + label] = hvar
        self.histograms.update(vardict)
        return
        
    def fillHistograms(self, leptons, jets, ev):
        """ Fill your histograms here. This also applies mur, muf variations following
        the recommend scheme from: https://twiki.cern.ch/twiki/bin/view/CMS/TopSystematics
            * mur fixed: vary muf by factor 2 (0.5) for up (down) variation
            * muf fixed: vary mur by factor 2 (0.5) for up (down) variation
            * combined: vary mur and muf by factors 2 (0.5) for up (down) variation.
            
        Indices:
            LHEScaleWeight[0] is MUF=0.5 MUR=0.5 
            LHEScaleWeight[1] is MUF=1.0 MUR=0.5 
            LHEScaleWeight[2] is MUF=2.0 MUR=0.5 
            LHEScaleWeight[3] is MUF=0.5 MUR=1.0 
            LHEScaleWeight[4] is MUF=1.0 MUR=1.0 
            LHEScaleWeight[5] is MUF=2.0 MUR=1.0 
            LHEScaleWeight[6] is MUF=0.5 MUR=2.0 
            LHEScaleWeight[7] is MUF=1.0 MUR=2.0 
            LHEScaleWeight[8] is MUF=2.0 MUR=2.0
             
        """
        
        # Initialize a weight
        weight = -99
        
        uncs = ["nom"]
        uncs.extend(self.uncs)
        for unc in uncs:
            for direction in ["nom", "up", "down"]:
                # Now we just need to select the proper weight
                label = "_%s_%s"%(unc, direction)

                # Case 1) Just use the nominal weight for nominal histograms
                if unc == "nom" and direction == "nom": 
                    weight = ev.genWeight
                    label = ""
                elif unc == "nom" and direction != "nom": 
                    continue
                elif unc != "nom" and direction == "nom": 
                    continue
                
                # Case 2) Factorization scale variations
                if unc == "scale" and direction == "up": 
                    weight = ev.genWeight * (ev.LHEScaleWeight[5]/ev.LHEScaleWeight[4])
                if unc == "scale" and direction == "down": 
                    weight = ev.genWeight * (ev.LHEScaleWeight[3]/ev.LHEScaleWeight[4])
                
                # Case 3) Renormalization scale variations
                if unc == "renorm" and direction == "up": 
                    weight = ev.genWeight * (ev.LHEScaleWeight[7]/ev.LHEScaleWeight[4])
                if unc == "renorm" and direction == "down": 
                    weight = ev.genWeight * (ev.LHEScaleWeight[1]/ev.LHEScaleWeight[4]) 
                    
                # Case 4) Combined scale variations
                if unc == "combined" and direction == "up": 
                    weight = ev.genWeight * (ev.LHEScaleWeight[8]/ev.LHEScaleWeight[4])
                if unc == "combined" and direction == "down": 
                    weight = ev.genWeight * (ev.LHEScaleWeight[0]/ev.LHEScaleWeight[4]) 
                
                # Lepton variables
                self.histograms["leadingLeptonPt" + label].Fill(leptons[0].pt, weight)   
                self.histograms["leadingLeptonEta" + label].Fill(leptons[0].eta, weight)  
                self.histograms["trailingLeptonPt" + label].Fill(leptons[1].pt, weight)  
                self.histograms["trailingLeptonEta" + label].Fill(leptons[1].eta, weight) 

                # To draw the composition of nJets as function of flavour
                self.histograms["Njet" + label].Fill(len(jets), weight)

                # Jet variables 
                self.histograms["leadingJetPt" + label].Fill(jets[0].pt if len(jets) >= 1 else -99, weight)   
                self.histograms["leadingJetEta" + label].Fill(jets[0].eta if len(jets) >= 1 else -99, weight)  
                self.histograms["trailingJetPt" + label].Fill(jets[1].pt if len(jets) >= 2 else -99, weight)  
                self.histograms["trailingJetEta" + label].Fill(jets[1].eta if len(jets) >= 2 else -99, weight) 
        return
        
    