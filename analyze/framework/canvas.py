# Code for getting a general canvas 
# used for producing CMS plots

import ROOT as r
import pandas as pd
import numpy as np
from copy import deepcopy
import sys, os, re
import array

r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)
pd.options.display.float_format = "{:,.2f}".format

class canvas(object):
   
   w = 600 
   h = 600

   p1_x1, p1_y1, p1_x2, p1_y2 = 0, 0.30, 1, 1
   p2_x1, p2_y1, p2_x2, p2_y2 = 0, 0, 1, 0.30

   p1_bottomMargin = 0.025
   p2_topMargin    = 0.06
   p2_bottomMargin = 0.3


   leg_width = 0.6
   leg_textsize = 0.042
   leg_columns = 3

   cmsprel_x1, cmsprel_y1, cmsprel_x2, cmsprel_y2 = .08, .91, .5, .97
   lumi_x1, lumi_y1, lumi_x2, lumi_y2 = .53, .91, .79, .97
   _noDelete = {}

   def __init__(self, name):
      self.name = name
      return    
   def SetLogy(self):
      self.p1.SetLogy()
      self.name = self.name+"_logY"
   def new_canvas(self, doRatio = True):
      if doRatio:
         c = r.TCanvas("c_%s"%(self.name), "", self.w, self.h)
         c.Divide(1, 2)
         p1 = c.GetPad(1)
         p1.SetPad(self.p1_x1, self.p1_y1, self.p1_x2, self.p1_y2)
         p1.SetTopMargin(p1.GetTopMargin()*1.1)
         p1.SetBottomMargin(self.p1_bottomMargin)

         p2 = c.GetPad(2)
         p2.SetPad(self.p2_x1, self.p2_y1, self.p2_x2, self.p2_y2)
         p2.SetTopMargin(self.p2_topMargin)
         p2.SetBottomMargin(self.p2_bottomMargin)

         self.c = c 
         self.p1 = p1
         self.p2 = p2
         return c, p1, p2
      else:
         c = r.TCanvas("c_%s"%(self.name), "", self.w, self.h)
         self.c = c
         return c

   def make_legend(self, x0, y0, x1, y1):                                                     
      l = r.TLegend(x0, y0, x1, y1)
      l.SetName("l_%s"%(self.name))
      l.SetBorderSize(0)
      l.SetFillColor(0)
      l.SetShadowColor(0)
      l.SetFillStyle(0)
      l.SetTextFont(42)
      l.SetTextSize(self.leg_textsize)
      l.SetNColumns(self.leg_columns)
      return l

   def doSpam_lumi(self, lumi):
      align=12 
      textSize=0.07
      text = "%3.2f fb^{-1} (13 TeV)"%lumi
      lumi = r.TPaveText(self.lumi_x1, self.lumi_y1, self.lumi_x2, self.lumi_y2,"NDC");
      lumi.SetTextSize(textSize);
      lumi.SetFillColor(0);
      lumi.SetFillStyle(0);
      lumi.SetLineStyle(2);
      lumi.SetLineColor(0);
      lumi.SetTextAlign(align);
      lumi.SetTextFont(42);
      lumi.AddText(text);
      self._noDelete[text] = lumi; ## so it doesn't get deleted by PyROOT
      return lumi

   def doSpam(self):
      align=12 
      textSize=0.07
      text = "#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}"
      cmsprel = r.TPaveText(self.cmsprel_x1, self.cmsprel_y1, self.cmsprel_x2, self.cmsprel_y2,"NDC");
      cmsprel.SetTextSize(textSize);
      cmsprel.SetFillColor(0);
      cmsprel.SetFillStyle(0);
      cmsprel.SetLineStyle(2);
      cmsprel.SetLineColor(0);
      cmsprel.SetTextAlign(align);
      cmsprel.SetTextFont(42);
      cmsprel.AddText(text);
      self._noDelete[text] = cmsprel; ## so it doesn't get deleted by PyROOT
      return cmsprel 

   def save_canvas(self, outpath):
      self.c.SaveAs(outpath+"/%s.png"%self.name)
      self.c.SaveAs(outpath+"/%s.pdf"%self.name)
      return


