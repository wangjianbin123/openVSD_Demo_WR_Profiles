# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:25:33 2015

@author: wangjianbin
"""
###############################################################################
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import interpolate
###############################################################################
dsktop='G:\\'
folder_path='cstest\\'
###############################################################################
def invert(d):
    a=np.array(d)
    l=len(a)
    temp=np.zeros((l,2),dtype=float)
    for ii in np.arange(0,l,1):
        temp[ii,0]=a[l-1-ii,0]
        temp[ii,1]=a[l-1-ii,1]
    data={'y':temp[:,0],'z':temp[:,1]}
    pdata=pd.DataFrame(data)
    return pdata
###############################################################################
# lwp_path=dsktop+folder_path+'wl.txt'
# rwp_path=dsktop+folder_path+'wr.txt'

lwp_path=dsktop+folder_path+'complete_s1002_325_l.txt'
rwp_path=dsktop+folder_path+'complete_s1002_325_r.txt'
leftwheel=pd.read_csv(lwp_path,sep='\s',names=['y','z'],engine='python')
rw=pd.read_csv(rwp_path,sep='\s',names=['y','z'],engine='python')
rightwheel=invert(rw)

lrp_path=dsktop+folder_path+'complete_uic60l.txt'
rrp_path=dsktop+folder_path+'complete_uic60r.txt'
leftrail=pd.read_csv(lrp_path,sep='\s',names=['y','z'],engine='python')
rr=pd.read_csv(rrp_path,sep='\s',names=['y','z'],engine='python')
rightrail=invert(rr)

## Contact Geometry File
contactgeo_path=dsktop+folder_path+'cps2.txt'
contactgeo=pd.read_csv(contactgeo_path,sep='\s',names=['y','leftwheels1','leftwheels2','leftrails1','leftrails2','rightwheels1','rightwheels2','rightrails1','rightrails2'],engine='python')
##############################################################################
lenleftwheel=len(leftwheel)
lenleftrail=len(leftrail)
lenrightwheel=len(rightwheel)
lenrightrail=len(rightrail)
###############################################################################
rd=0.46
# leftwheelsp=interpolate.InterpolatedUnivariateSpline(leftwheel.y,leftwheel.z-rd)
# rightwheelsp=interpolate.InterpolatedUnivariateSpline(rightwheel.y,rightwheel.z-rd)

leftwheelsp=interpolate.InterpolatedUnivariateSpline(leftwheel.y,leftwheel.z)
rightwheelsp=interpolate.InterpolatedUnivariateSpline(rightwheel.y,rightwheel.z)

leftrailsp=interpolate.InterpolatedUnivariateSpline(leftrail.y,leftrail.z)
rightrailsp=interpolate.InterpolatedUnivariateSpline(rightrail.y,rightrail.z)

wheelpntinterval=500
railpntinterval=500
lwpnty=np.linspace(leftwheel['y'][0],leftwheel['y'][lenleftwheel-1],wheelpntinterval)
lwpntz=leftwheelsp(lwpnty)
##
rwpnty=np.linspace(rightwheel['y'][0],rightwheel['y'][lenrightwheel-1],wheelpntinterval)
rwpntz=rightwheelsp(rwpnty)
##
lrpnty=np.linspace(leftrail['y'][0],leftrail['y'][lenleftrail-1],railpntinterval)
lrpntz=leftrailsp(lrpnty)
##
rrpnty=np.linspace(rightrail['y'][0],rightrail['y'][lenrightrail-1],railpntinterval)
rrpntz=rightrailsp(rrpnty)
###############################################################################
## plot module
mpl.rcParams['font.size']=30
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.serif'] = ['Times New Roman'] + plt.rcParams['font.serif']
mpl.rcParams['figure.figsize']=(19,7)
mpl.rcParams['figure.dpi']=600
fig1,ax1=plt.subplots(1,1)
##optimal plots
ax1.yaxis.set_ticklabels('')
ax1.yaxis.set_ticks_position('none')
ax1.xaxis.set_ticklabels('')
ax1.xaxis.set_ticks_position('none')
## line width
wrwidth=2
contlinewidth=1
##wheel rail profiles shift values
wpcordis=1.50
rpcordis=1.506
shiftval=0.678
liftval=0.012
## plot wheel and rail profiles#################################
mpl.rcParams['lines.linewidth']=wrwidth
plt1=ax1.plot(lwpnty+wpcordis/2.0-shiftval,-1.0*lwpntz+liftval,'k',rwpnty-wpcordis/2.0+shiftval,-1.0*rwpntz+liftval,'k',lrpnty+rpcordis/2.0-shiftval,lrpntz,'r',rrpnty-rpcordis/2.0+shiftval,rrpntz,'r',antialiased=0)
#plt1=ax1.plot(lwpnty+wpcordis/2.0-shiftval,-1*lwpntz+liftval,'k',rwpnty-wpcordis/2.0+shiftval,-1*rwpntz+liftval,'k',antialiased=0)
ax1.set_ylim(-0.04,0.05)
ax1.set_xlim(-0.16,0.16)
plt.yticks()
################################################################
##plot contact lines############################################
movnum=len(contactgeo)
mpl.rcParams['lines.linewidth']=contlinewidth
for movindex in np.arange(0,movnum,1):
    lx=np.array((2,1),dtype=float)
    ly=np.array((2,1),dtype=float)
    ly[0]=leftwheelsp(contactgeo['leftwheels1'][movindex])*(-1.0)+liftval
    lx[0]=contactgeo['leftwheels1'][movindex]+wpcordis/2.0-shiftval
    ly[1]=leftrailsp(contactgeo['leftrails2'][movindex])
    lx[1]=contactgeo['leftrails2'][movindex]+rpcordis/2.0-shiftval
    ##right w-r contact pnts
    rx=np.array((2,1),dtype=float)
    ry=np.array((2,1),dtype=float)
    ry[0]=rightwheelsp(contactgeo['rightwheels1'][movindex])*(-1.0)+liftval
    rx[0]=contactgeo['rightwheels1'][movindex]-wpcordis/2.0+shiftval
    ry[1]=rightrailsp(contactgeo['rightrails2'][movindex])
    rx[1]=contactgeo['rightrails2'][movindex]-rpcordis/2.0+shiftval
    ax1.plot(lx,ly,'k',rx,ry,'k',alpha=1)
###############################################################################
##plot contact point index
shiftnum=15
halfshift=int(shiftnum/2)
lowband=-0.001*float(halfshift)
highband=0.001*float(halfshift)
leftlinex=np.linspace(-0.07,0.07,shiftnum)+0.075
leftliney=np.linspace(0.03,0.03,shiftnum)
ax1.plot(leftlinex,leftliney,lw=1.5,c='g')
for posindex in np.arange(0,shiftnum,1):
    ax1.text(leftlinex[posindex],leftliney[posindex],str(int(posindex-halfshift)),fontsize=30,fontfamily='serif')
rightlinex=np.linspace(0.07,-0.07,shiftnum)-0.075
rightliney=np.linspace(0.03,0.03,shiftnum)
ax1.plot(rightlinex,rightliney,lw=1.5,c='g')
for posindex in np.arange(0,shiftnum,1):
    ax1.text(rightlinex[posindex],rightliney[posindex],str(-1*int(posindex-halfshift)),fontsize=30,fontfamily='serif')
##plot contact pnt indication lines
leftcontactpnt={'movy':np.array(contactgeo['y']),'profy':np.array(contactgeo['leftwheels1'])}
rightcontactpnt={'movy':np.array(contactgeo['y']),'profy':np.array(contactgeo['rightwheels1'])}
leftcontactpoint=pd.DataFrame(leftcontactpnt)
rightcontactpoint=pd.DataFrame(rightcontactpnt)
lstdmovy=np.linspace(lowband,highband,shiftnum)
rstdmovy=np.linspace(lowband,highband,shiftnum)
deltay=leftcontactpoint.movy[1]-leftcontactpoint.movy[0]
##
ii=0
for kk in lstdmovy:
    ind=int((kk-leftcontactpoint.movy[0])/deltay)
    lwprofy=leftcontactpoint.profy[ind]
    lwy=leftwheelsp(lwprofy)*(-1.0)+liftval
    lwx=lwprofy+wpcordis/2.0-shiftval
    indx=leftlinex[::-1][ii]
    indy=leftliney[::-1][ii]
    lx=np.array((2,1),dtype=float)
    ly=np.array((2,1),dtype=float)
    lx[0]=lwx
    lx[1]=indx
    ly[0]=lwy
    ly[1]=indy
    ax1.plot(lx,ly,c='b',lw=1,alpha=0.75)
    ii+=1
##
jj=0
for mm in rstdmovy:
    ind=int((mm-rightcontactpoint.movy[0])/deltay)
    rwprofy=rightcontactpoint.profy[ind]
    rwy=rightwheelsp(rwprofy)*(-1.0)+liftval
    rwx=rwprofy-wpcordis/2.0+shiftval
    indx=rightlinex[jj]
    indy=rightliney[jj]
    rx=np.array((2,1),dtype=float)
    ry=np.array((2,1),dtype=float)
    rx[0]=rwx
    rx[1]=indx
    ry[0]=rwy
    ry[1]=indy
    ax1.plot(rx,ry,c='b',lw=1,alpha=0.75)
    jj+=1
##
fig1_savepath=dsktop+folder_path+'contact_points.jpeg'
fig1.savefig(fig1_savepath,dpi=1200)