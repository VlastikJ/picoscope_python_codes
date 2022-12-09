# -*- coding: utf-8 -*-
#
"""




@author: Vlastimil
"""
#import novevyhodnoceni as vhd
import numpy as np
import matplotlib.pyplot as plt
#import os.path as op
from picoscope_3000a_runblock import naberData
from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TH1F,TString,TGraph
import time
#import ROOT
# 1 SAMPLE = (12/245) us              

rozsah = 50 #mV
kolo_1 = 5
kolo_2 = 9

step = 1
hist_r = TH1F("rozlozeni_amp"," ",rozsah*step,0,rozsah*step)

sum = []
 
capt =  1000
starttime = time.time()
endtime = 0.1 #pocet minut jak dlouho pojede mereni 
while time.time() < starttime + endtime*60:
    napeti, n_samples = naberData('50 mV',capt,2)
    napeti = -napeti
    napeti = napeti.transpose()
    name_napeti = "napeti_{}.root".format(cislo)
    file2 = TFile(name_napeti, "recreate", "recreate")
    print(napeti.shape)
    for i in range(0,len(napeti)):
        max_V = np.max(napeti[i])
        sum.append(np.sum(napeti[i]))
        for j in range(0,len(napeti[i])):
            if napeti[i,j]>0:
                print(napeti[i,j])
            hist_r.Fill(napeti[i,j],1)
        #hn.Write()
    file2.Close()
    max_I = np.max(sum)
    n_bins = int(max_I*10)
    hist_S = TH1F("suma_napeti"," ",n_bins,0,max_I)
    for i in range(0,len(sum)):
        hist_S.Fill(sum[i],1) 
    name_hist = "hist_{}_{}_{}.root".format(capt,kolo_1,kolo_2)
    file = TFile(name_hist, "recreate", "recreate")
    hist_r.Write()
    hist_S.Write()
    file.Close()
    start_pause = time.time()
