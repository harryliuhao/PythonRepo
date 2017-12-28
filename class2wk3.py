# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 21:06:36 2017

@author: Hao Liu
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as st

np.random.seed(12345)
mean_hypo=42500
ind=np.arange(4) #number of years

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
df
df=df.transpose()

interval_95=st.t.interval(0.95, len(df)-1, loc=np.mean(df), scale=st.sem(df))
yerr_95=(interval_95[1]-interval_95[0])/2
mean_df=df.mean()

bar_color=pd.Series('grey',index=range(4)) #define default color to grey

fig=plt.figure()

barlist=plt.bar(ind,mean_df,width=0.5,yerr=yerr_95,error_kw=dict(lw=1, capsize=5, capthick=1))

for i in range(0,len(interval_95[1])):
    barlist[i].set_color(bar_color[i]) #set default color
    if interval_95[1][i]<mean_hypo:
        barlist[i].set_color('blue') #override default if outside boundary
    if interval_95[0][i]>mean_hypo:
        barlist[i].set_color('red')  #override default if outside boundary 

plt.axhline(y=mean_hypo, c='green',label='hypothesis')
plt.xticks(ind,('1992','1993','1994','1995'))
plt.xlabel('Year')
plt.ylabel('Sample Mean')
plt.title('hypothesis test of sample mean (95% confidence interval)')
plt.legend(loc = 2, frameon = False)
plt.show()


