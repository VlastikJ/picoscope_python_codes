# -*- coding: utf-8 -*-
#
"""




@author: Vlastimil
"""
#import novevyhodnoceni as vhd
import numpy as np
import matplotlib.pyplot as plt
#import os.path as op
from picoscope_5000a_runblock import naberData_5
import datetime as dt
from ROOT import TCanvas, TPad, TFile, TPaveLabel, TPaveText, TH1F,TString
import time
#import ROOT
# 1 SAMPLE = (12/245) us              

rozsah = 10 #mV
capt =  10000
kolo_1 = 5
kolo_2 = 10
n_bins = 10000

#0 jis for disable sec channel
sec_C_range = '2 V'

sum = []
amp = []



starttime = time.time()
endtime = 2 #pocet minut jak dlouho pojede mereni 

hist_r = TH1F("rozlozeni_amp"," ",n_bins,-rozsah,rozsah)
while time.time() < starttime + endtime*60:
    napeti, n_samples = naberData_5('10 mV',capt,3,sec_C_range)
    napeti = -napeti
    napeti = napeti.transpose()
    x = list(range(0,n_samples))
    for i in range(0,len(napeti)):
        
        amp.append(np.max(napeti[i]))
        sum.append(np.sum(napeti[i]))
        for j in range(0,len(napeti[i])):            
            hist_r.Fill(napeti[i,j],1)
            
    start_pause = time.time()
    
max_I = np.max(sum)
min_I= np.min(sum)
max_A = np.max(amp)
min_A= np.min(amp)
hist_A = TH1F("max_napeti"," ",n_bins,min_A-1,max_A+1)
hist_S = TH1F("suma_napeti"," ",n_bins,min_I-10,max_I+10)
for i in range(0,len(sum)):
    hist_S.Fill(sum[i],1) 
    
for i in range(0,len(amp)):
    hist_A.Fill(amp[i],1) 
date = dt.datetime.now()
name_hist = "hist_{}_{}_{}_{}.root".format(capt,kolo_1,kolo_2,date)
file = TFile(name_hist, "recreate", "recreate")
hist_r.Write()
hist_S.Write()
hist_A.Write()
file.Close()
    
