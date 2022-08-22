# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 16:28:30 2021

@author: lenovo
"""
######################################
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib as mpl
#from scipy import interpolate
#######################################

base_path='G:\\cstest\\reduced_test\\'
file_name='reducted_reducted_reducted_complete_s1002_325_l.txt'
reduction='reducted_'+file_name
file_path=base_path+file_name

#######################################
data=pd.read_csv(file_path,sep='\s',names=['y','z'],engine='python')
l = len(data)
half_l=int(l/2)
new=np.zeros((half_l,2),dtype=float)
for i in np.arange(0,half_l,1):
    new[i][0]=data.y[2*i]
    new[i][1]=data.z[2*i]
newdata=pd.DataFrame(new,columns=['y','z'])
#######################################
np.savetxt(reduction,new)