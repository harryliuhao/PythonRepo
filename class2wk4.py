# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 21:30:38 2017

@author: Hao Liu
"""

import os
import pandas as pd
import numpy as np
import xlrd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime, timedelta

#parameters
homedir='C:/Users/Hao Liu/Documents/2_python/PythonRepo'
file_election='presidential_election_results.csv'
file_party='presidents_party.csv'

os.chdir(homedir)

#read source files to df
df_results=pd.read_csv(file_election, usecols=['Year','Candidates'])
df_party=pd.read_csv(file_party)


df_results['name']=df_results['Candidates'].apply(lambda x: re.search('(^.*)won',x).group(1).strip())
df_results['percent']=df_results['Candidates'].apply(lambda x: re.search('(\d+)%',x).group(1))

#fix naming discrepancies between datasets
dic_candidates = {'Bush and Cheney': "George W. Bush", 'Dwight D. Eisenhower': 'Dwight Eisenhower', 'Harry S. Truman':'Harry Truman',
       'Lyndon B. Johnson': 'Lyndon Johnson','Ronald W. Reagan':'Ronald Reagan', 'Dole and Kemp': 'Bob Dole',
       'Hillary R. Clinton':'Hillary Clinton', 'John W. Davis':'John Davis', 'George Bush':'George H. Bush'}

df_results.replace({"name": dic_candidates}, inplace=True)
df_party.replace({"president": dic_candidates}, inplace=True)

#add candidates that won Virginia and lost in national results
df_candidates = pd.DataFrame([['Hillary Clinton', 'Democrat'], ['Bob Dole', 'Republican'],['John Davis', 'Democrat']], columns=['president','party'])
df_party=df_party.append(df_candidates)

df_party_change=pd.merge(df_results,df_party,left_on='name',right_on='president',how='left')
df_party_change['party_color']=np.where(df_party_change.party=='Republican','red','blue')

df_party_change['percent']=df_party_change.percent.apply(pd.to_numeric)

sns.factorplot(x='Year', y='percent', palette=reversed(df_party_change['party_color']), kind='bar',data=df_party_change, size=6, aspect=1.6)


"""
Question: Is Virginia a battleground state or blue/Democrat state?

Analysis:
On the United States election map, there are several swing states dubbed as "battleground" states because they can go either ways, Republican or Democrat. In US politics, Democrat party is generally associated with color "blue" and Republican with color 'red'. Virginia used to be considered as a battleground state.

Having living in Virginia for over 17 years, it still puzzles me what is state's color in the general elections, so I take this opportunity to look back at the historical presidential election results in Virginia. 

In this chart, the bar color is corresponding to the party color. The Y-axis is the percentage of the ballot that the candidate won. Any results significantly higher than 50% is considered an overwhelming victory. 

In the grand picture since 1924, Virginia is a battleground state. Democrats FDR/Harry Truman dominated the WWII era elections, followed by a long dominance from 1968 through 2004 by Republicans. Since then, the tide has turned again favoring Democrats with Barack Obama's two victories. In the latest 2016 general election, Hilary Clinton won the state but lost the national election.

It is true the demographic change in Northern Virginia/Fairfax country is increasingly deterministic to the state election results. Looking at recent Virginia election demographic map, most of the Virginia counties are 'red', and only several counties are 'blue', and yet these several 'urban' counties still dominated the state's election results. However, we should note that neither party has an over 60% winning percentage in the last seven elections. Democrat's victories in the last three cycles have seen a declining advantage.

If you really want to know why Virginia is still swinging? My two cents are Virginian cares more about the person, less of their parties.  
"""