### Class to store information about samples 
import json
from framework.analyzer import analyzer
import framework.particles as particles
import ROOT as r 

  
  def make_pretty_histo(self, h):
    ## We just need to fix bin labels and those kind of things. Most of configurations
    ## (xtitle, binning, etc...) is already applied.
    h.SetLineColor(eval("r.%s"%self.color))  
    h.GetYaxis().SetTitleFont(42)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleOffset(2)
    h.GetYaxis().SetLabelFont(42)
    h.GetYaxis().SetLabelSize(0.05)
    h.GetYaxis().SetLabelOffset(0.007)
    h.SetMaximum(h.GetMaximum()*1.3)
    h.GetYaxis().SetTitle("Normalized events")
    h.SetLineWidth(2)
    h.SetLineStyle(1)
    return

  def dress_histograms(self):
    for hname, h in self.histos.items():
      self.make_pretty_histo(h)
    return

  def get_histo(self, hname):
    return self.histos[hname]
  
  def get_histonames(self):
    return self.histos.keys()

  def analyze(self):
    # create an analyzer
    self.analyzer = analyzer(self.rfile, self.histAxisName)
    self.histos = self.analyzer.get_histograms()
    # Apply some cosmetics to the histograms
    self.dress_histograms()
    return    
    
