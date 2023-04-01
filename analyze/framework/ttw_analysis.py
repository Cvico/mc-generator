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

    def loop(self):
        """ Here you have to implement your own analysis """
        # Read the input tree
        rfile = r.TFile.Open(self.fname)
        t = self.tree_events 
   
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
            if not( len(jets) >= 2 ): continue
            if not( len(leptons) >= 2): continue
            if not(leptons[0].pt > 25): continue
            if not(leptons[1].pt > 20): continue
            if not(leptons[0].pdgId*leptons[1].pdgId>0): continue
            if not(len(leptons) == 2): continue 
            
            # Fill histograms
            self.fillHistograms(leptons, jets, ev)

        rfile.Close()
        return
    
    
    

    