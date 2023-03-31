""" This is the main analyzer """
from framework.particles import lepton_obj, jet_obj
import ROOT as r
import numpy as np
import os, sys
from copy import deepcopy

class baseAnalyzer(object):
    def __init__(self, options, file_):
        # Save information in attributes
        self.inputFolder = options.inputFolder
        self.nEvents = options.nEvents
        self.outpath = options.outpath
        self.file = file_

        self.fname = os.path.join(self.inputFolder, self.file)


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
  
    def progressBar(self, count_value, total, suffix=''):
        """ Just a silly progress bar to debug if the code is running """
        bar_length = 100
        filled_up_Length = int(round(bar_length* count_value / float(total)))
        percentage = round(100.0 * count_value/float(total),1)
        bar = '=' * filled_up_Length + '-' * (bar_length - filled_up_Length)
        sys.stdout.write('[%s] %s%s ...%s\r' %(bar, percentage, '%', suffix))
        sys.stdout.flush()
        return
  
