# -- Import libraries -- #
import ROOT as r
import numpy as np
import os
from framework.functions import get_files
from framework.histogram import histogram
from optparse import OptionParser
from copy import deepcopy

# -- Define functions -- #
def add_parsing_opts():
    """ Function with base parsing arguments used by any script """
    parser = OptionParser(usage = "python nanogen_analysis.py [options]", 
                        description = "Main options for running nanogen analysis") 
    parser.add_option("--inputFolder", dest = "inputFolder", default = "outfiles",
                help = "Input file to run the analysis.")
    parser.add_option("--outputFolder", dest = "outpath", default = "outplots",
                help = "Output folder to store plots.")
    parser.add_option("--mcaFile", dest = "mcaFile", default = "mca.txt",
                help = "File with information samples.")
    return parser

_nodelete = {}
def new_label(text, x0,y0,x1,y1, textSize):
    align=12 
    textSize=0.07
    label = r.TPaveText(x0,y0,x1,y1, "NDC");
    label.SetTextSize(textSize)
    label.SetFillColor(0)
    label.SetFillStyle(0)
    label.SetLineStyle(2)
    label.SetLineColor(0)
    label.SetTextAlign(align)
    label.SetTextFont(42)
    label.AddText(text)
    return label

def divide_histos(hnum, hden_input, color):
    # Remove error from the denominator
    hden = deepcopy(hden_input)
    for bini in range(1, 1+hden.GetNbinsX()+1):
        hden.SetBinError(bini, 0)
    hratio = deepcopy(hnum.Clone(hnum.GetName()+"_ratio"))
    hratio.Divide(hden)
    hratio.SetLineColor(color)
    hratio.SetLineWidth(1)
    hratio.SetFillColorAlpha(color, 1)
    hratio.SetFillStyle(1001)
    hratio.SetMarkerColor(color)
    hratio.SetMarkerStyle(20)
    return hratio
    
def plot(files, opts, plotname):
    # From here on everything is hardcoded simply because it's easier to organise
    # and this is a very specific analysis...
    
    central_qcut42      = histogram(files["central_qCut42_hists"], opts.inputFolder, plotname)
    central_qcut150     = histogram(files["central_qCut150_hists"], opts.inputFolder, plotname)
    ttW_gennano_qcut42  = histogram(files["ttW_gennano_qcut42_hists"], opts.inputFolder, plotname)
    ttW_gennano_qcut150 = histogram(files["ttW_gennano_qcut150_hists"], opts.inputFolder, plotname)

    # Nominal histograms:
    hnom_central_qcut42      = central_qcut42.get_nom_histo()     
    hnom_central_qcut150     = central_qcut150.get_nom_histo()
    hnom_ttW_gennano_qcut42  = ttW_gennano_qcut42.get_nom_histo()
    hnom_ttW_gennano_qcut150 = ttW_gennano_qcut150.get_nom_histo()
    
    
    # Histograms with total uncertainty (scale+stat)
    hscaleunc_central_qcut42      = central_qcut42.get_scale_histo()     
    hscaleunc_central_qcut150     = central_qcut150.get_scale_histo()
    hscaleunc_ttW_gennano_qcut42  = ttW_gennano_qcut42.get_scale_histo()
    hscaleunc_ttW_gennano_qcut150 = ttW_gennano_qcut150.get_scale_histo()
    
    # -- Get all the ratios for the second pad
    hratio_scaleunc_central_qcut42      = divide_histos(hscaleunc_central_qcut42, hnom_central_qcut42, central_qcut42.color)
    hratio_scaleunc_central_qcut150     = divide_histos(hscaleunc_central_qcut150, hnom_central_qcut150, central_qcut150.color)
    hratio_scaleunc_ttW_gennano_qcut42  = divide_histos(hscaleunc_ttW_gennano_qcut42, hnom_ttW_gennano_qcut42, ttW_gennano_qcut42.color)
    hratio_scaleunc_ttW_gennano_qcut150 = divide_histos(hscaleunc_ttW_gennano_qcut150, hnom_ttW_gennano_qcut150, ttW_gennano_qcut150.color)
    
    # -- Get all the ratios for the third pad
    hratio_totalunc_central_qcut150     = divide_histos(hnom_central_qcut150, hnom_central_qcut42, central_qcut150.color)
    hratio_totalunc_ttW_gennano_qcut42  = divide_histos(hnom_ttW_gennano_qcut42, hnom_central_qcut42, ttW_gennano_qcut42.color)
    hratio_totalunc_ttW_gennano_qcut150 = divide_histos(hnom_ttW_gennano_qcut150, hnom_central_qcut42, ttW_gennano_qcut150.color)
    
    # Create a legend:
    l = r.TLegend(0.58, 0.68, 0.78, 0.88)
    l.SetName("l_%s"%(plotname))
    l.SetBorderSize(0)
    l.SetFillColor(0)
    l.SetShadowColor(0)
    l.SetFillStyle(0)
    l.SetTextFont(42)
    l.SetTextSize(0.042)
    l.SetNColumns(1)    
    l.AddEntry(hnom_central_qcut42, "Central (Q = 42 GeV)", "l")
    l.AddEntry(hnom_central_qcut150, "Central (Q = 150 GeV)", "l")
    l.AddEntry(hnom_ttW_gennano_qcut42, "FxFx@1j (Q = 42 GeV)", "l")
    l.AddEntry(hnom_ttW_gennano_qcut150, "FxFx@1j (Q = 150 GeV)", "l")

    # Now start plotting things
    # Some labels:
    cmsprel   = new_label( "#bf{CMS} Internal", .08, .91, .5, .97 ,0.07)
    lab_scale = new_label( "scale unc.", .78, .81, .89, .92, 0.3)
    lab_ratio = new_label( "ratio", 0.78, .81, .89, .92, 0.3)

    c = r.TCanvas("c_%s"%(plotname), "", 800, 1200)
    c.Divide(1, 3)
    p1 = c.GetPad(1)
    p1.SetPad(0, 0.55, 1, 1)
    p1.SetBottomMargin(0)

    p2 = c.GetPad(2)
    p2.SetPad(0, 0.35, 1, 0.55)
    p2.SetTopMargin(0)
    p2.SetBottomMargin(0)
 
    p3 = c.GetPad(3)
    p3.SetPad(0, 0.05, 1, 0.35)
    p3.SetTopMargin(0)
    p3.SetBottomMargin(0.28)
    
    p1.cd()
    hnom_central_qcut42.Draw("hist")
    hnom_central_qcut42.GetYaxis().SetNdivisions(505)
    hnom_central_qcut42.GetXaxis().SetLabelSize(0)
    hnom_central_qcut150.Draw("hist same")    
    hnom_ttW_gennano_qcut150.Draw("hist same") 
    hnom_ttW_gennano_qcut42.Draw("hist same")
    cmsprel.Draw("same")
    l.Draw("same")
    
    unity = deepcopy(hnom_central_qcut42.Clone("unity_%s"%plotname))
    for bini in range(1, unity.GetNbinsX()+1):
        unity.SetBinContent(bini, 1)
    unity.SetLineColor(r.kBlack)
    
    p2.cd()
    hratio_scaleunc_central_qcut150.GetYaxis().SetTitleSize(0.15)
    hratio_scaleunc_central_qcut150.GetYaxis().SetTitleOffset(0.7)
    hratio_scaleunc_central_qcut42.Draw("e2")
    hratio_scaleunc_central_qcut42.GetYaxis().SetRangeUser(0.6, 1.4)
    hratio_scaleunc_central_qcut42.GetYaxis().SetNdivisions(505)
    hratio_scaleunc_central_qcut42.GetYaxis().SetLabelSize(0.1)
    hratio_scaleunc_central_qcut42.GetXaxis().SetLabelSize(0)
    hratio_scaleunc_central_qcut150.GetYaxis().SetTitle("Scale uncertainty")
    


    hratio_scaleunc_central_qcut150.Draw("e2 same ")
    hratio_scaleunc_ttW_gennano_qcut150.Draw("e2 same")
    hratio_scaleunc_ttW_gennano_qcut42.Draw("e2 same")
    hratio_scaleunc_central_qcut42.SetFillColorAlpha(hratio_scaleunc_central_qcut42.GetFillColor(), 0.4)
    unity.Draw("hist same")
    lab_scale.Draw("same")
    

    
    p3.cd()  
    hratio_totalunc_central_qcut150.GetXaxis().SetTitleSize(0.05)
    hratio_totalunc_central_qcut150.Draw("pe1")
    hratio_totalunc_central_qcut150.GetYaxis().SetTitle("Ratio")
    hratio_totalunc_central_qcut150.GetYaxis().SetTitleSize(0.1)

    hratio_totalunc_central_qcut150.GetYaxis().SetRangeUser(0.5, 1.5)
    hratio_totalunc_central_qcut150.GetYaxis().SetNdivisions(505)
    hratio_totalunc_central_qcut150.GetYaxis().SetLabelSize(0.1)
    hratio_totalunc_central_qcut150.GetXaxis().SetLabelSize(0.1)
    hratio_totalunc_central_qcut150.GetYaxis().SetLabelSize(0.06)

    counter = 2
    if plotname == "Njet":
        for bini in range(1, 1+hratio_totalunc_central_qcut150.GetNbinsX()):
            hratio_totalunc_central_qcut150.GetXaxis().SetBinLabel(bini, "%d"%counter)
            counter += 1
    hratio_totalunc_central_qcut150.GetXaxis().CenterLabels()
    hratio_totalunc_central_qcut150.GetXaxis().SetTitleOffset(1.1)
    hratio_totalunc_central_qcut150.GetXaxis().SetTitleSize(0.12)
 
    hratio_totalunc_ttW_gennano_qcut42.Draw("pe1 same") 
    hratio_totalunc_ttW_gennano_qcut150.Draw("pe1 same")
    unity.Draw("hist same")
  
    lab_ratio.Draw("same")  
    if not os.path.exists(opts.outpath):
        os.system("mkdir -p %s"%opts.outpath)
    c.SaveAs("%s/%s.png"%(opts.outpath, plotname))
    c.SaveAs("%s/%s.pdf"%(opts.outpath, plotname))
    return


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
    print(files)
    for plotname in plots:
        plot(files, opts, plotname)