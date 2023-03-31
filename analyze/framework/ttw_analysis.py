""" This is the main analyzer """
from framework.particles import lepton_obj, jet_obj
from framework.baseAnalyzer import baseAnalyzer
import ROOT as r
import numpy as np
import os
from framework.functions import *
from copy import deepcopy

# Cuts for the selection here

class ttw_analysis(baseAnalyzer):
    debug = True
    order_by_pt = lambda self, x: x.pt
    
    def createHistograms(self):
        """ Here you define what histograms are plotted """
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

        return

    def loop(self):
        """ Here you have to implement your own analysis """
        # Read the input tree
        rfile = r.TFile.Open(self.fname)
        t = rfile.Get("Events")
        maxevents = min(t.GetEntries(), self.nEvents)
        
        print(">> Processing file: %s"%self.fname)
        print("   * Reading %d events"%self.nEvents)
        
        # Perform the sequential analysis
        for iev, ev in enumerate(t):
            if iev > maxevents: break # Cutre but it works :) 

            leptons = []
            jets    = []

            # Silly progress bar
            if iev%(maxevents/10) == 0: self.progressBar(iev, maxevents, "(%d/%d)"%(iev, maxevents))

            
            # Select leptons --> pt1 >= 25 GeV, pt2 >= 25 GeV; within tracker
            nLeptons = ev.nGenDressedLepton
            nSelLeptons = 0
            leptons = []
            for il in range(nLeptons):
                pt = ev.GenDressedLepton_pt[il]
                eta = ev.GenDressedLepton_eta[il]
                phi = ev.GenDressedLepton_phi[il]
                pdgId = ev.GenDressedLepton_pdgId[il]
                hasTauAnc = ev.GenDressedLepton_hasTauAnc[il]
                
                ell = lepton_obj(pt, eta, phi, pdgId, hasTauAnc)
                
                if ell.pt >= 20 and abs(ell.eta) <= 2.5: leptons.append(ell)

                
            # Select jets --> pt >= 25 within tracker            
            nJets = ev.nGenJet
            jets = []
            for ij in range(nJets):
                pt = ev.GenJet_pt[ij]
                eta = ev.GenJet_eta[ij]
                phi = ev.GenJet_phi[ij]
                partonFlavour = ev.GenJet_partonFlavour[ij]
                hadronFlavor = ev.GenJet_hadronFlavour[ij]
                jet = jet_obj(pt, eta, phi, partonFlavour, hadronFlavor)
                if pt >= 25 and eta <= 2.5: jets.append(jet)

            # Now clean the jets 
            nbJet = 0
            for ilep, lep in enumerate(leptons):
                philep = lep.phi
                etalep = lep.eta
                for ijet, jet in enumerate(jets):
                    phijet = jet.phi
                    etajet = jet.eta
                    de     = etajet - etalep
                    dp     = deltaPhi(philep, phijet)
                    deltaR = np.sqrt(de*de + dp*dp)
                    if deltaR < 0.4: 
                        jets.remove(jet)
                    if jet.partonFlavour == 5: 
                        nbJet += 1

            ## Order by pT 
            leptons.sort(key = self.order_by_pt, reverse=True)
            jets.sort(key = self.order_by_pt, reverse=True)

            ### SELECTIONS ###
            if not( nbJet >= 1 ): continue    
            if not( len(jets) >= 3 ): continue
            if not( len(leptons) >= 2): continue
            if not(leptons[0].pt > 25): continue
            if not(leptons[1].pt > 20): continue
            if not(leptons[0].pdgId*leptons[1].pdgId>0): continue
            if not(len(leptons) == 2): continue 
            
            # Fill histograms
            self.fillHistograms(leptons, jets, ev)

        rfile.Close()
        return
    
    def fillHistograms(self, leptons, jets, ev):
        """ Fill your histograms here """
        weight = ev.genWeight

        # Lepton variables
        self.histograms["leadingLeptonPt"].Fill(leptons[0].pt, weight)   
        self.histograms["leadingLeptonEta"].Fill(leptons[0].eta, weight)  
        self.histograms["trailingLeptonPt"].Fill(leptons[1].pt, weight)  
        self.histograms["trailingLeptonEta"].Fill(leptons[1].eta, weight) 

        # To draw the composition of nJets as function of flavour
        self.histograms["Njet"].Fill(len(jets), weight)

        # Jet variables 
        self.histograms["leadingJetPt"].Fill(jets[0].pt if len(jets) >= 1 else -99, weight)   
        self.histograms["leadingJetEta"].Fill(jets[0].eta if len(jets) >= 1 else -99, weight)  
        self.histograms["trailingJetPt"].Fill(jets[1].pt if len(jets) >= 2 else -99, weight)  
        self.histograms["trailingJetEta"].Fill(jets[1].eta if len(jets) >= 2 else -99, weight) 

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