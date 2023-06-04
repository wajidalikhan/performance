import os, subprocess, yaml, glob
from math import sqrt
from collections import OrderedDict
from Constants import Constants
from printing_utils import *
from tdrstyle_JME import *
import tdrstyle_JME as TDR
rt.gROOT.SetBatch(rt.kTRUE)
rt.gStyle.SetOptStat(0)
rt.gStyle.SetOptFit(0)

def MakeRatioHistograms(h1, h2, name):
    hratio = h1.Clone(name)
    for bin in range(1,h1.GetNbinsX()+1):
        r, dr = (0,0)
        num = h1.GetBinContent(bin)
        den = h2.GetBinContent(bin) 
        if den!=0 and num!=0:
            r = num/den
            dr = r*oplus(h1.GetBinError(bin)/num,h2.GetBinError(bin)/den)
        hratio.SetBinContent(bin, r)
        hratio.SetBinError(bin, dr)
    return hratio
