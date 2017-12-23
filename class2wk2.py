# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 12:57:51 2017

@author: Hao Liu
"""

import matplotlib.pyplot as plt
import pandas as pd
import os

os.chdir('C:/Users/Hao Liu/Documents/2_python/PythonRepo')
df=pd.read_csv('wk2.csv')
df_local=df[-df.Date.str.contains('02-29')]

df_local=df_local[df_local.Date<'2015-01-01']
df_local['dayofyear']=df_local.Date.str.extract('[-](\d{2}-\d{2})')
#covert Date to datatime
df_local.Date=list(map(pd.to_datetime, df_local.Date))

#separate df two separate low and high dfs
df_min=df_local[df_local['Element']=='TMIN']
df_max=df_local[df_local['Element']=='TMAX']
df_min.drop(['ID','Element'], axis=1, inplace=True)
df_max.drop(['ID','Element'], axis=1, inplace=True)
df_min.rename(columns={'Data_Value': 'record_low'}, inplace=True)
df_max.rename(columns={'Data_Value': 'record_high'}, inplace=True)

df_max_all=df_max.groupby('dayofyear',sort=True)['record_high'].max()
df_min_all=df_min.groupby('dayofyear',sort=True)['record_low'].min()

df_min_all.columns=['dayofyear','record_low']

plt.figure()
plt.plot(df_min_all.dayofyear,df_min.record_low,'-o',df_max.dayofyear,df_max.record_high,'-o',alpha=0.3)