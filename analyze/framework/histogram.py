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
        hunc = deepcopy(hvar)
        for bini in range(1, 1+hunc.GetNbinsX()):
            # Uncertainty corresponds to the difference between nominal and variation
            unc = abs(nom.GetBinContent(bini) - hvar.GetBinContent(bini))
            
            # Get the statistical error in the nominal bin
            stat = nom.GetBinError(bini)
            total_unc = np.sqrt(stat**2 + unc**2)
            hunc.SetBinContent(bini, total_unc)

        
        # Save the histogram in the main dictionary
        self.histograms["_".join(plot.split("_")[-2:])] = hunc
        return
    
    def compute_total_var(self):
        nom = self.histograms["nominal"]
        for direction in ["up", "down"]:
            for bini in range(1, 1+nom.GetNbinsX()):
                # Fill the one with all the uncertainties
                scale = self.histograms["scale_%s"%direction].GetBinContent(bini)
                renorm = self.histograms["renorm_%s"%direction].GetBinContent(bini)
                combined = self.histograms["combined_%s"%direction].GetBinContent(bini)
                #total_unc = max(scale, renorm, combined)
                total_unc = np.sqrt(scale**2 + renorm**2 + combined**2)
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
        self.compute_total_var() 
 
    def dress_histograms(self):
        # Decorate the nominal histogram
        self.histograms["nominal"].SetLineColor(self.color)  
        self.histograms["nominal"].GetYaxis().SetTitleFont(42)
        self.histograms["nominal"].GetYaxis().SetTitleSize(0.05)
        self.histograms["nominal"].GetYaxis().SetTitleOffset(2)
        self.histograms["nominal"].GetYaxis().SetLabelFont(42)
        self.histograms["nominal"].GetYaxis().SetLabelSize(0.05)
        self.histograms["nominal"].GetYaxis().SetLabelOffset(0.007)
        self.histograms["nominal"].SetMaximum(self.histograms["nominal"].GetMaximum()*1.3)
        self.histograms["nominal"].SetLineWidth(2)
        self.histograms["nominal"].SetLineStyle(1)
        
        # Decorate the uncertainty histogram
        hunc = deepcopy(self.histograms["nominal"])
        hunc.SetLineColor(self.color)
        hunc.SetLineWidth(0)
        hunc.SetFillColorAlpha(self.color, 1)
        hunc.SetFillStyle(1001)
        
        for bini in range(1, hunc.GetNbinsX()+1):
            hunc.SetBinContent(bini, 1)
        
        self.histograms["total_unc"] = hunc
        return
    
    def get_nom_histo(self):
        return self.histograms["nominal"]
    
    def get_unc_histo(self):
        return self.histograms["total_unc"]
    
    def get_ratio_histo(self, h):
        hratio = deepcopy(self.histograms["nominal"].Clone(self.histograms["nominal"].GetName()+"_ratio"))
        hratio.SetMarkerStyle(20)
        hratio.SetMarkerSize(1)
        hratio.SetMarkerColor(self.color)
        hratio.Divide(h)
        return hratio
    
    def normalize_histogram(self):
        self.histograms["nominal"].Scale(1/self.norm)
        return


        