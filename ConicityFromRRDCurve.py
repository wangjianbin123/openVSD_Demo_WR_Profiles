# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 00:04:21 2015
@author: wang jianbin

compute equivalent conicity from OOVSD data
"""
###############################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import interpolate
from scipy import integrate
###############################################################################
dsktop='G:\\'
folder_path='cstest\\'
rrd_path=dsktop+folder_path+'rrd2.txt'
radiusdiff=pd.read_csv(rrd_path,sep='\s',names=['y','d'],engine='python')
rrdsp=interpolate.InterpolatedUnivariateSpline(np.array(radiusdiff.y),np.array(radiusdiff.d))
posindic=radiusdiff.loc[radiusdiff['d']>=0].index[::-1][0]
pospnt=radiusdiff.iloc[posindic,0]
negindic=radiusdiff.loc[radiusdiff['d']<=0].index[0]
negpnt=radiusdiff.iloc[negindic,0]
balancepnt=(pospnt+negpnt)/2.0
##
ldis=balancepnt-radiusdiff['y'][0]
rdis=radiusdiff['y'][:-1][0]-balancepnt
if ldis>=rdis:
    stdconicitydis=rdis
if ldis<rdis:
    stdconicitydis=ldis
###############################################################################
leftwheelradius=0.460
rightwheelradius=0.460
rd=1.5
polachpnt=200
polachend=0.006
##############################################################################
balancedradiusdiff=radiusdiff.copy()
balancedradiusdiff['y']-=balancepnt
balancedrrdsp=interpolate.InterpolatedUnivariateSpline(np.array(balancedradiusdiff.y),np.array(balancedradiusdiff.d))
polachspace=np.linspace(0.0001,polachend,polachpnt)
polachresults=np.zeros((polachpnt,2),dtype=float)
for pindex in np.arange(0,polachpnt,1):
    polachresults[pindex,0]=polachspace[pindex]*1000
    factor=-1.0/(2*np.pi*polachspace[pindex])
    polachresults[pindex,1]=factor*integrate.quad(lambda x:balancedrrdsp(polachspace[pindex]*np.sin(x))*np.sin(x),0,2*np.pi)[0]
polachsp=interpolate.InterpolatedUnivariateSpline(np.array(polachresults[:,0]),np.array(polachresults[:,1]))
polacheqconicity=pd.DataFrame(polachresults,columns=['y','ec'])
###############################################################################
mpl.rcParams['lines.linewidth']=2
mpl.rcParams['figure.figsize']=(8,6)
fig0,ax0=plt.subplots(1,1)
ax0.plot(polacheqconicity.y,polacheqconicity.ec,'k-')
ax0.grid()
###############################################################################
mpl.rcParams['lines.linewidth']=2
mpl.rcParams['figure.figsize']=(8,6)
fig1,ax1=plt.subplots(1,1)
ax1.plot(radiusdiff.y*1000,radiusdiff.d*1000,'k-')
ax1.grid()
###############################################################################