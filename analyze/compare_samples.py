# -- Import libraries -- #
import ROOT as r
import numpy as np
from framework.ttw_analysis import ttw_analysis
from framework.canvas import canvas
from framework.functions import get_files
from framework.histogram import histogram

import json
from copy import deepcopy
import os
from optparse import OptionParser
import multiprocessing as mp


# -- Define functions -- #
def add_parsing_opts():
  """ Function with base parsing arguments used by any script """
  parser = OptionParser(usage = "python nanogen_analysis.py [options]", 
                        description = "Main options for running nanogen analysis") 
  parser.add_option("--inputFolder", dest = "inputFolder", default = "outfiles",
              help = "Input file to run the analysis.")
  parser.add_option("--mcaFile", dest = "mcaFile", default = "mca.txt",
              help = "File with information samples.")
  return parser

if __name__ == "__main__":
  ## Now start plotting things
  plots = ["Njet", 
           "leadingLeptonPt", "leadingLeptonEta", 
           "leadingJetPt", "leadingJetEta", 
           "trailingLeptonPt", "trailingLeptonEta", 
           "trailingJetEta", "trailingJetPt"]
  
  parser = add_parsing_opts()
  (opts, args) = parser.parse_args()
  
  files = get_files(opts)
  counter = 0
  for filename, fileinfo in files.items():
    histogram(fileinfo, opts.inputFolder, "Njet")
    if counter == 1: break
    counter += 1
    
  '''
  for plot in plots:
    # ============================================== Now another normalizing to xsec
    canv = canvas(plot+"_normalizedToXsec")
    c1,p1,p2 = canv.new_canvas()
    l1 = canv.make_legend(.60, .6, .78, .88)
    l1.SetNColumns(1)
    cmsprel = canv.doSpam()

    l2 = canv.make_legend(.60, .7, .88, .88)
    l2.SetNColumns(1)


    # temporal:  
    fqcut150 = r.TFile.Open("./outrootfiles/ttw_gennanoSergio_qcut150_hist.root")
    fqcut42 = r.TFile.Open("./outrootfiles/ttw_gennanoSergio_qcut42_hist.root")
    fcentral = r.TFile.Open("./outrootfiles/TTWToLNu_central_hist.root")

    h_qcut150 = deepcopy(fqcut150.Get(plot)) 
    #h_qcut150.Scale(1.14/h_qcut150.Integral())
    h_qcut150.Scale(1/679.2)
    h_qcut150.SetLineColor(r.kRed+1)
    h_stat_qcut50 = deepcopy(h_qcut150)
    h_stat_qcut50.SetLineWidth(0)
    h_stat_qcut50.SetFillColorAlpha(r.kRed+1, 0.4)
    h_stat_qcut50.SetFillStyle(3004)

    h_qcut42 = deepcopy(fqcut42.Get(plot)) 
    #h_qcut42.Scale(1.14/h_qcut42.Integral())
    h_qcut42.Scale(1/679.2)
    h_qcut42.SetLineColor(r.kCyan+1)
    h_stat_qcut42 = deepcopy(h_qcut42)
    h_stat_qcut42.SetLineWidth(0)
    h_stat_qcut42.SetFillColorAlpha(r.kCyan+1, 0.4)
    h_stat_qcut42.SetFillStyle(3004)

    h_central = deepcopy(fcentral.Get(plot)) 
    #h_central.Scale(1/h_central.Integral())
    h_central.Scale(1/592.) 
    h_central.SetLineColor(r.kBlack)
    h_stat_central = deepcopy(h_central)
    h_stat_central.SetLineWidth(0)
    h_stat_central.SetFillColorAlpha(r.kBlack, 0.4)
    h_stat_central.SetFillStyle(3004)


    print("Events from FxFx@1J (qCut = 42 GeV): %3.2f (histogram normalized to 679.2 fb-1) "%(h_qcut150.Integral()*679.2))
    print("Events from FxFx@1J (qCut = 150 GeV, pT = 60): %3.2f (histogram normalized to 679.2 fb-1)"%(h_qcut42.Integral()*679.2))
    print("Events from Central: %3.2f (histogram normalized to 592 fb-1)"%(h_central.Integral()*592))

    l1.AddEntry(h_qcut150, "FxFx@1J (qCut = 150 GeV)","l")
    l1.AddEntry(h_qcut42, "FxFx@1J (qCut = 42 GeV)", "l")  
    l1.AddEntry(h_central, "Central", "l")  

    h_ratio_qcut150 = deepcopy(h_qcut150.Clone("ratio_%s_new"%plot))
    h_ratio_qcut42 = deepcopy(h_qcut42.Clone("ratio_%s_old"%plot))
    h_ratio_central = deepcopy(h_central.Clone("ratio_%s_nloqcd"%plot))

    h_ratio_qcut150.Divide(h_central)
    h_ratio_qcut150.SetMarkerSize(1)
    h_ratio_qcut150.SetMarkerStyle(20)
    h_ratio_qcut150.SetLineColor(r.kRed+1)
    h_ratio_qcut150.SetMarkerColor(r.kRed+1)

    h_ratio_qcut42.Divide(h_central)
    h_ratio_qcut42.SetMarkerSize(1)
    h_ratio_qcut42.SetMarkerStyle(20)
    h_ratio_qcut42.SetLineColor(r.kCyan+1)
    h_ratio_qcut42.SetMarkerColor(r.kCyan+1)

    h_ratio_central.Divide(h_central)

#    h_ratio.GetYaxis().SetRangeUser(max(h_ratio.GetMinimum()*0.9,  0.1), min(h_ratio.GetMaximum()*1.1, 1.9))
    h_ratio_qcut150.GetYaxis().SetRangeUser(0.1, 2.3)
    h_ratio_qcut150.GetYaxis().SetNdivisions(505)
    h_ratio_qcut150.GetXaxis().SetLabelSize(0.1)
    h_ratio_qcut150.GetXaxis().SetTitleSize(0.05)
    h_ratio_qcut150.GetXaxis().SetTitleOffset(h_ratio_qcut150.GetXaxis().GetTitleOffset()*1.2)
    h_ratio_qcut150.GetXaxis().SetTitleSize(0.1)
    h_ratio_qcut150.GetYaxis().SetTitle("New/central")
    h_ratio_qcut150.GetYaxis().SetTitleOffset(1.1)
    h_ratio_qcut150.GetYaxis().SetTitleSize(0.05)
    h_ratio_qcut150.GetYaxis().SetTitleSize(0.05)


    # ==== DRAW ON FIRST CANVAS ==== #
    p1.cd()
    h_qcut150.GetYaxis().SetRangeUser(0., max([h_qcut150.GetMaximum(), h_central.GetMaximum()])*1.1)
    h_qcut150.Draw("hist")
    h_qcut150.GetYaxis().SetRangeUser(0., max([h_qcut150.GetMaximum(), h_central.GetMaximum()])*1.1)
    h_central.Draw("hist same")
    h_qcut42.Draw("hist same")
    h_stat_qcut50.Draw("e2 same")
    h_stat_qcut42.Draw("e2 same")
    h_stat_central.Draw("e2 same")
    h_qcut150.SetMaximum(h_qcut150.GetMaximum()*1.2)
    h_qcut150.GetYaxis().SetTitle("Events")
    h_qcut150.GetXaxis().SetLabelSize(0)
    cmsprel.Draw("same")
    l1.Draw("same")

    # ==== DRAW ON SECOND CANVAS ==== #
    p2.cd()
    h_ratio_qcut150.Draw("pe1")
    h_ratio_qcut150.SetMarkerSize(1)
    h_ratio_qcut150.SetMarkerStyle(20)
    h_ratio_qcut150.GetYaxis().SetRangeUser(0.5, 1.5)

    h_ratio_qcut150.GetYaxis().SetNdivisions(505)
    h_ratio_qcut150.SetMarkerColor(r.kRed+1)
    h_ratio_qcut42.Draw("pe1 same")
    h_ratio_qcut42.SetMarkerSize(1)
    h_ratio_qcut42.SetMarkerStyle(20)
    h_ratio_central.Draw("hist same")
    if not os.path.exists(outpath): os.mkdir(outpath)
    canv.save_canvas(outpath)
  '''