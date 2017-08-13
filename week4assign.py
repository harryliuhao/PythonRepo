# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import os
import sys
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import re
from scipy.stats import ttest_ind

os.chdir('C:/Users/Hao Liu/Documents/2_python/PythonRepo')
 
# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

fname='university_towns.txt'

dfTemp = pd.DataFrame([line.rstrip('\n') for line in open(fname)])
dfTemp.columns=['lineName']
 
#find state name rows that have a unique regex pattern
dfTemp['TownFlag']=0
dfTemp.loc[dfTemp['lineName'].str.contains('\w+\[edit\]'),'TownFlag']=1
#create state column and forward fill NaN values
dfTemp['State']=dfTemp['lineName'].where(dfTemp['TownFlag']==1)
dfTemp['State']=dfTemp['State'].str.replace('\[edit\]','')      
dfTemp['State'].ffill(inplace=True)
 
#create RegionName column
reRegionPat=" \(.*|\[.*"
dfTemp['RegionName']=dfTemp['lineName'].where(dfTemp['TownFlag']==0)
dfTemp['RegionName']=dfTemp['RegionName'].str.replace(reRegionPat,'')
dfTemp['RegionName']=dfTemp['RegionName'].str.strip()

#keep only two columns
dfTown=dfTemp.loc[dfTemp['TownFlag']==0,['State','RegionName']]
dfTown.reset_index(inplace=True)
dfTown['index']=range(1,518)
dfTown.set_index('index',inplace=True)
dfTown['State'].replace(regex=True,inplace=True,to_replace=r'[^a-zA-Z]+',value=r'')

dfTown.head(20)

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    fname='university_towns.txt'

    dfTemp = pd.DataFrame([line.rstrip('\n') for line in open(fname)])
    dfTemp.columns=['lineName']

    #find state name rows that have a unique regex pattern
    dfTemp['TownFlag']=0
    dfTemp.loc[dfTemp['lineName'].str.contains('\w+\[edit\]'),'TownFlag']=1
    #create state column and forward fill NaN values
    dfTemp['State']=dfTemp['lineName'].where(dfTemp['TownFlag']==1)
    dfTemp['State']=dfTemp['State'].str.replace('\[edit\]','')      
    dfTemp['State'].ffill(inplace=True)

    #create RegionName column
    reRegionPat=" \(.*|\[.*"
    dfTemp['RegionName']=dfTemp['lineName'].where(dfTemp['TownFlag']==0)
    dfTemp['RegionName']=dfTemp['RegionName'].str.replace(reRegionPat,'')
    dfTemp['RegionName']=dfTemp['RegionName'].str.strip()
    #keep only two columns
    dfTown=dfTemp.loc[dfTemp['TownFlag']==0,['State','RegionName']]
    dfTown.reset_index(inplace=True)
    dfTown['index']=range(517) #reset index to consecutive numbers
    dfTown.set_index('index',inplace=True)
    dfTown['State'].replace(regex=True,inplace=True,to_replace=r'^[^a-zA-Z]+',value=r'') #remove special characters at the beginning

    return dfTown
#testing
dfTest=get_list_of_university_towns()
len(dfTest)
dfTest.groupby('State').count()
dfTest.tail(10)
 
#read gdp data
gdpfile='gdplev.xls'
dfTemp=pd.read_excel(gdpfile,skiprows=4,header=1)
dfTemp=dfTemp.iloc[2:,[4,6]]
dfTemp.columns=['Quarter','GDP']
 
dfGDP=dfTemp[dfTemp['Quarter']>'1999q4']
dfGDP['Growth']=dfGDP['GDP'].pct_change()
 
#flag recession quarters

dfTemp=dfGDP.copy()        

#recession start
for i in range(1,len(dfGDP)):
    if dfGDP.iloc[i-1,2]>0 and dfGDP.iloc[i,2]<0 and dfGDP.iloc[i+1,2]<0: print(dfGDP.iloc[i,0])      

def get_recession_start():
    for i in range(1,len(dfGDP)):
        if dfGDP.iloc[i-1,2]>0 and dfGDP.iloc[i,2]<0 and dfGDP.iloc[i+1,2]<0: return (dfGDP.iloc[i,0])    
    


#recession end
for i in range(1,len(dfGDP)):
    if dfGDP.iloc[i-3,2]<0 and dfGDP.iloc[i-2,2]<0 and dfGDP.iloc[i-1,2]>0 and dfGDP.iloc[i,2]>0: print(dfGDP.iloc[i,0]) 


def get_recession_end():
    for i in range(1,len(dfGDP)):
        if dfGDP.iloc[i-3,2]<0 and dfGDP.iloc[i-2,2]<0 and dfGDP.iloc[i-1,2]>0 and dfGDP.iloc[i,2]>0: return (dfGDP.iloc[i,0]) 
     
get_recession_start()
get_recession_end()


IndexEnd=dfGDP[dfGDP['Quarter']==get_recession_end()].index[0] #ending index loc
dfTrough=dfGDP.loc[IndexEnd-2]#loc uses index, opposed to iloc using row number
dfTrough['Quarter']

def get_recession_bottom():
    IndexEnd=dfGDP[dfGDP['Quarter']==get_recession_end()].index[0] #ending index loc
    #lowest GDP is the period that last the last negative growth rate
    dfTrough=dfGDP.loc[IndexEnd-2]#loc uses index, opposed to iloc using row number
    return dfTrough['Quarter']

get_recession_bottom()

dfTemp=pd.read_csv(csvfile)
dfColumn=dfTemp.iloc[:,6:].columns.values #monthly columns starts at :6
dfColumn=dfColumn[(dfColumn>'2000') & (dfColumn<'2016-10')] #get thr range of columns to convert to quarters
dfMonthly=dfTemp.loc[:,dfColumn] #separate monthly data columns from main df
dfQuarterly=pd.concat([dfMonthly.iloc[:,i:i+3].mean(axis=1) for i in range(0, len(dfMonthly.columns),3)],axis=1) #I still don't fully understand pd.concat yet

ListYear=list(range(2000,2017))
ListQuarter=['q1','q2','q3','q4']#observe those two lines on different syntax to construct a list
ListColumnName=[]
for i in ListYear:
    for j in ListQuarter:
        ListColumnName.append(str(i)+j)

ListColumnName=ListColumnName[:-1:1] #use -1 to remove the last extra column
dfQuarterly.columns=ListColumnName

dfHousing=pd.concat([dfTemp[['State','RegionName']],dfQuarterly],axis=1) #two dfs being concat need to be in a list as input for pd.concat
dfHousing.replace({'State':states},inplace=True)
dfHousing.set_index(['State','RegionName'],inplace=True)
dfHousing.head()

def convert_housing_data_to_quarters():
    csvfile='City_Zhvi_AllHomes.csv'
    dfTemp=pd.read_csv(csvfile)
    dfColumn=dfTemp.iloc[:,6:].columns.values #monthly columns starts at :6
    dfColumn=dfColumn[(dfColumn>'2000') & (dfColumn<'2016-10')] #get thr range of columns to convert to quarters
    dfMonthly=dfTemp.loc[:,dfColumn] #separate monthly data columns from main df
    dfQuarterly=pd.concat([dfMonthly.iloc[:,i:i+3].mean(axis=1) for i in range(0, len(dfMonthly.columns),3)],axis=1) #I still don't fully understand pd.concat yet
    
    ListYear=list(range(2000,2017))
    ListQuarter=['q1','q2','q3','q4']#observe those two lines on different syntax to construct a list
    ListColumnName=[]
    for i in ListYear:
        for j in ListQuarter:
            ListColumnName.append(str(i)+j)
    
    ListColumnName=ListColumnName[:-1:1] #use -1 to remove the last extra column
    dfQuarterly.columns=ListColumnName
    
    dfHousing=pd.concat([dfTemp[['State','RegionName']],dfQuarterly],axis=1) #two dfs being concat need to be in a list as input for pd.concat
    dfHousing.replace({'State':states},inplace=True)
    dfHousing.set_index(['State','RegionName'],inplace=True)
    
    return dfHousing


start=get_recession_start()
bottom=get_recession_bottom()
dfHousingPrice=convert_housing_data_to_quarters()
dfRecession=dfHousingPrice.loc[:,start:bottom]
dfRecession.reset_index(inplace=True)
dfTown=get_list_of_university_towns()
dfTown['UniTown']=1

dfRecession['Growth']=(dfRecession[bottom]-dfRecession[start])/dfRecession[start]
dfRecession=pd.merge(dfRecession,dfTown,on=['State','RegionName'],how='left')

dfTownPrice=dfRecession[dfRecession['UniTown']==1]
dfNoTownPrice=dfRecession[dfRecession['UniTown']!=1]

dfTown=dfTownPrice['Growth'].dropna()
dfNoTown=dfNoTownPrice['Growth'].dropna()

if dfTown.mean()> dfNoTown.mean():
    better='university town'
else:
    better='non-university town'

pVal=list(ttest_ind(dfNoTown,dfTown))[1]

if pVal<0.01:
    different=True
else:
    different=False

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    start=get_recession_start()
    bottom=get_recession_bottom()
    dfHousingPrice=convert_housing_data_to_quarters()
    dfRecession=dfHousingPrice.loc[:,start:bottom]
    dfRecession.reset_index(inplace=True)
    dfTown=get_list_of_university_towns()
    dfTown['UniTown']=1
    
    dfRecession['Growth']=(dfRecession[bottom]-dfRecession[start])/dfRecession[start]
    dfRecession=pd.merge(dfRecession,dfTown,on=['State','RegionName'],how='left')
    
    dfTownPrice=dfRecession[dfRecession['UniTown']==1]
    dfNoTownPrice=dfRecession[dfRecession['UniTown']!=1]
    
    dfTown=dfTownPrice['Growth'].dropna()
    dfNoTown=dfNoTownPrice['Growth'].dropna()
    
    if dfTown.mean()> dfNoTown.mean():
        better='university town'
    else:
        better='non-university town'
    
    pVal=list(ttest_ind(dfNoTown,dfTown))[1]
    
    if pVal<0.01:
        different=True
    else:
        different=False
    return (different,pVal,better)

run_ttest()
