# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 12:17:26 2017

@author: Hao Liu
"""

import pandas as pd
import numpy as np
import os

os.getcwd()
os.chdir('C:/Users/Hao Liu/Documents/2_python')

def df_clean(data):
    newData = ''.join([i for i in data if not i.isdigit()])
    i = newData.find('(')
    if i>-1: newData = newData[:i]
    return newData.strip()

"""import the first dataset"""
df=pd.read_excel("Energy Indicators.xls",skiprows=17,skip_footer=38,na_values='...')
energy=df.iloc[:,2:6]
energy.columns=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
energy['Energy Supply']=energy['Energy Supply']*1000000.0

energy['Country'] = energy['Country'].apply(df_clean)
di = {"Republic of Korea": "South Korea",
"United States of America": "United States",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China, Hong Kong Special Administrative Region": "Hong Kong"}
energy.replace({"Country": di},inplace = True)


"""import the gdp dataset"""
gdp=pd.read_csv("API_NY.GDP.MKTP.CD_DS2_en_csv_v2.csv",skiprows=3)
di={"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"}
gdp.replace({"Country Name":di},inplace=True)
gdp.rename(columns={'Country Name':'Country'},inplace=True)
gdp10=gdp.loc[:,['Country','Country Code','Indicator Name','Indicator Code','2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]

"""import the index dataset"""
ScimEn=pd.read_excel("scimagojr.xlsx")
ScimEn15=ScimEn[ScimEn["Rank"]<16]

"""merge"""
df=pd.merge(pd.merge(energy,gdp10,on='Country'),ScimEn15,on='Country')
df.set_index('Country',inplace=True)
df=df.loc[:,['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]

def answer_one():
    return df

test=answer_one()
test.shape

"""question 2"""
outer=pd.merge(pd.merge(energy,gdp,on='Country',how='outer'),ScimEn,on='Country',how='outer')

def answer_two():
    return len(outer)-len(df)

test=answer_two()
test

"""question 3"""

def col_mean(df):
    data=df[]
    return pd.Series({'avgGDP':np.mean(data)})




Top15 = answer_one()
cols=['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
test=Top15[cols].mean(axis=1).sort_values(ascending=False).rename('avgGDP')
test

def answer_three():
    Top15 = answer_one()
    cols=['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    test=Top15[cols].mean(axis=1).sort_values(ascending=False).rename('avgGDP')
    return test

'find the No 6 index value, which is France
No6=answer_three()
No6name=No6[No6==No6[5]].index.values

'slice the Top15 using the index value
No6_df=Top15[Top15.index.values==No6name]
No6_df['2015']-No6_df['2006']

Top15['Energy Supply per Capita'].mean()
Top15['% Renewable'].max()
