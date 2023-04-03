""" This is for common formatting of histograms """
from framework.particles import lepton_obj, jet_obj
import ROOT as r
import numpy as np
import os, sys
from copy import deepcopy

class histogram(object):
    def __init__(self, fileinfo, inputFolder, plot):
        self.filename = fileinfo["file"]
        self.norm = float(fileinfo["norm"])
        self.color = fileinfo["color"]
        self.useForRatio = fileinfo["useForRatio"]
        self.legend = fileinfo["legend"]
        self.inputFolder = inputFolder
        self.plot = plot  
        self.get_histograms()
        self.normalize_histogram()
        self.dress_histograms()
        return
    
    def compute_var(self, f, nom, plot):
        hvar = deepcopy(f.Get(plot))
        for bini in range(1, 1+hvar.GetNbinsX()):
            # Uncertainty corresponds to the difference between nominal and variation
            unc = abs(nom.GetBinContent(bini) - hvar.GetBinContent(bini))
            hvar.SetBinContent(bini, unc)
     
        # Save the histogram in the main dictionary
        self.histograms["_".join(plot.split("_")[-2:])] = hvar
        return
    
    def compute_scale_variation(self):
        """ Create a histogram with only the scale uncertainties """
        nom_withScale_vars = deepcopy(self.histograms["nominal"].Clone("onlyscale_%s"%self.filename))
        for bini in range(1, 1+nom_withScale_vars.GetNbinsX()):
            # Fill the one with all the uncertainties
            scale_up = self.histograms["scale_up"].GetBinContent(bini)
            renorm_up = self.histograms["renorm_up"].GetBinContent(bini)
            combined_up = self.histograms["combined_up"].GetBinContent(bini)
            
            scale_down = self.histograms["scale_down"].GetBinContent(bini)
            renorm_down = self.histograms["renorm_down"].GetBinContent(bini)
            combined_down = self.histograms["combined_down"].GetBinContent(bini)
            
            scale    = (scale_up+scale_down)/2.0
            renorm   = (renorm_up+renorm_down)/2.0
            combined = (combined_up+combined_down)/2.0
            
            unc = max(scale, renorm, combined)#np.sqrt(scale**2 + renorm**2 + combined**2)
            nom_withScale_vars.SetBinError(bini, unc)
                
        self.histograms["nom_withScaleVars"] = nom_withScale_vars
        return
    
    def compute_total_unc(self):
        """ Create a histogram with the total uncertainty """
        nom = self.histograms["nominal"]
        nom_withScale_vars = self.histograms["nom_withScaleVars"]
        for bini in range(1, 1+nom.GetNbinsX()):
            # Fill the one with all the uncertainties
            stat = nom.GetBinError(bini)
            scale = nom_withScale_vars.GetBinError(bini)
            total_unc = np.sqrt(stat**2 + scale**2)
            nom.SetBinError(bini, total_unc)
        return
    
    def get_histograms(self):
        self.histograms = {}

        f = r.TFile.Open("./%s/%s.root"%(self.inputFolder, self.filename))
        
        # Nominal histogram
        nom = deepcopy(f.Get(self.plot))
        self.histograms["nominal"] = nom
        
        # Variations
        self.compute_var(f, nom, self.plot + "_scale_up")
        self.compute_var(f, nom, self.plot + "_scale_down")
        self.compute_var(f, nom, self.plot + "_renorm_up")
        self.compute_var(f, nom, self.plot + "_renorm_down")
        self.compute_var(f, nom, self.plot + "_combined_up")
        self.compute_var(f, nom, self.plot + "_combined_down")
        
        # Total variations
        self.compute_scale_variation()
        self.compute_total_unc()
        return 
    
    def dress_histograms(self):
        # Decorate the nominal histogram
        self.histograms["nominal"].SetLineColor(self.color)  
        self.histograms["nominal"].GetYaxis().SetTitleFont(42)
        self.histograms["nominal"].GetYaxis().SetTitleSize(0.05)
        self.histograms["nominal"].GetYaxis().SetTitleOffset(1.05)
        self.histograms["nominal"].GetYaxis().SetLabelFont(42)
        self.histograms["nominal"].GetYaxis().SetLabelSize(0.05)
        self.histograms["nominal"].GetYaxis().SetLabelOffset(0.007)
        self.histograms["nominal"].SetMaximum(self.histograms["nominal"].GetMaximum()*1.3)
        self.histograms["nominal"].SetLineWidth(2)
        self.histograms["nominal"].SetLineStyle(1)
        return
    
    def get_nom_histo(self):
        return self.histograms["nominal"]
    
    def get_scale_histo(self):
        return self.histograms["nom_withScaleVars"]
    
    def normalize_histogram(self):
        self.histograms["nominal"].Scale(1/self.norm)
        self.histograms["nom_withScaleVars"].Scale(1/self.norm)
        return


        