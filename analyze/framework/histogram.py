""" This is for common formatting of histograms """
from framework.particles import lepton_obj, jet_obj
import ROOT as r
import numpy as np
import os, sys
from copy import deepcopy

class histogram(object):
    def __init__(self, fileinfo, inputFolder, plot):
        self.filename = fileinfo["file"]
        self.norm = fileinfo["norm"]
        self.color = fileinfo["color"]
        self.useForRatio = fileinfo["useForRatio"]
        self.inputFolder = inputFolder
        self.plot = plot
        
        self.get_histograms()
        
        self.histograms = {}
        return
    
    def compute_var(self, f, nom, plot):
        hvar = deepcopy(f.Get(plot))
        hunc = deepcopy(hvar)
        print(plot)
        for bini in range(1, 1+hunc.GetNbinsX()):
            # Uncertainty corresponds to the difference between nominal and variation
            unc = abs(nom.GetBinContent(bini) - hvar.GetBinContent(bini))/nom.GetBinContent(bini)
            
            # Get the statistical error in the nominal bin
            stat = nom.GetBinError(bini)/nom.GetBinContent(bini)
            print(bini, "stat: %3.4f"%stat, "variation: %3.4f"%unc)
        print("----")
    def compute_total_var(self):
        return
    
    def get_histograms(self):
        f = r.TFile.Open("./%s/%s.root"%(self.inputFolder, self.filename))
        
        # Nominal histogram
        nom = f.Get(deepcopy(self.plot))
        
        # Variations
        self.compute_var(f, nom, self.plot + "_scale_up")
        self.compute_var(f, nom, self.plot + "_scale_down")
        self.compute_var(f, nom, self.plot + "_renorm_up")
        self.compute_var(f, nom, self.plot + "_renorm_down")
        self.compute_var(f, nom, self.plot + "_combined_up")
        self.compute_var(f, nom, self.plot + "_combined_down")
        
        # Total variations
        self.compute_total_var() 
 
        

        