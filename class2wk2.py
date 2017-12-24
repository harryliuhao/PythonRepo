# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 12:57:51 2017

@author: Hao Liu
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from datetime import datetime

os.chdir('C:/Users/Hao Liu/Documents/2_python/PythonRepo')
df=pd.read_csv('wk2.csv',usecols=['ID', 'Date', 'Element','Data_Value'])
df_local=df[-df.Date.str.contains('02-29')]

df_2015_prior=df_local[df_local.Date<'2015-01-01']
df_2015=df_local[df_local.Date>='2015-01-01']

def max_min(df_local):
    df_local['dayofyear']=df_local.Date.str.extract('[-](\d{2}-\d{2})')
    
    #separate df two separate low and high dfs
    df_min=df_local[df_local['Element']=='TMIN']
    df_max=df_local[df_local['Element']=='TMAX']
    
    df_max_all=df_max.groupby('dayofyear',sort=True)['Data_Value'].max()
    df_min_all=df_min.groupby('dayofyear',sort=True)['Data_Value'].min()
    
    return df_max_all, df_min_all

max_2015_prior,min_2015_prior=max_min(df_2015_prior)
max_2015,min_2015=max_min(df_2015)

max_2015_index=np.where(max_2015.values>max_2015_prior.values)
min_2015_index=np.where(min_2015.values<min_2015_prior.values)


plt.figure(num=None, figsize=(12, 8), dpi=80, facecolor='w',  edgecolor=None)
plt.plot(max_2015_prior.values, 'orange', label = 'Historic High')
plt.plot(min_2015_prior.values, 'blue', label = 'Historic Low')
plt.gca().fill_between(range(len(max_2015_prior)), 
                       min_2015_prior.values, max_2015_prior.values, 
                       facecolor='grey', 
                       alpha=0.25)

plt.xticks(range(0, len(max_2015_prior), 30),max_2015_prior.index[range(0, len(max_2015_prior), 30)], rotation = '45')
plt.scatter(max_2015_index, max_2015.iloc[max_2015_index], s = 20, c='red', label = '2015 Record High')
plt.scatter(min_2015_index, min_2015.iloc[min_2015_index], s = 20, c='purple', label = '2015 Record Low')
plt.legend(loc = 8, frameon = False)
plt.xlabel('Day of the Year')
plt.ylabel('Temperature (Tenths of Degrees C)')
plt.title('Northen Virginia Temperature Records')
plt.tick_params(top='off', bottom='on', left='on', right='off', labelleft='on', labelbottom='on')
for spine in plt.gca().spines.values():
    spine.set_visible(False)
plt.show()