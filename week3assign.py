# -*- coding: utf-8 -*-
"""
Created on Sat Aug  5 12:17:26 2017

@author: Hao Liu
"""

import pandas as pd
import numpy as np
import os

os.getcwd()
os.chdir('C:/Users/Hao Liu/Documents/2_python/PythonRepo')

def df_clean(data):
    df = ''.join([i for i in data if not i.isdigit()])
    i = df.find('(')
    if i>-1: df = df[:i]
    return df.strip()

"""import the first dataset"""

def answer_one():
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

    return df

test=answer_one()
test.shape

"""question 2"""


def answer_two():
    df=answer_one()
    outer=pd.merge(pd.merge(energy,gdp,on='Country',how='outer'),ScimEn,on='Country',how='outer')
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

test=answer_three()
test
#find the No 6 index value, which is France
No6=answer_three()
No6name=No6[No6==No6[5]].index.values

#slice the Top15 using the index value
No6_df=Top15[Top15.index.values==No6name]
No6_df['2015']-No6_df['2006']

"""question 4"""
def answer_four():
    Top15 = answer_one()
    #find the No 6 index value, which is France
    No6=answer_three()
    No6name=No6[No6==No6[5]].index.values
    
    #slice the Top15 using the index value
    No6_df=Top15[Top15.index.values==No6name]
    
    return (No6_df['2015']-No6_df['2006'])


test=answer_four()
type(np.arange(test, dtype=np.float)[0])
type(np.float64(test))

"""question 5"""
def answer_five():
    Top15 = answer_one()
    
    return (Top15['Energy Supply per Capita'].mean())

test=answer_five()
test

"""question 6"""
test=Top15.sort_values('% Renewable',ascending=False).iloc[0]
test.name

def answer_six():
    Top15 = answer_one()
    test=Top15.sort_values('% Renewable',ascending=False).iloc[0]
    return (test.name,test['% Renewable'])

test=answer_six()
test

"""question 7"""
Top15['ct-ratio']=Top15['Self-citations']/Top15['Citations'] 
temp=Top15.sort_values(by='ct-ratio',ascending=False).iloc[0]
temp.name

def answer_seven():
    Top15 = answer_one()
    Top15['ct-ratio']=Top15['Self-citations']/Top15['Citations'] 
    temp=Top15.sort_values(by='ct-ratio',ascending=False).iloc[0]
    return (temp.name,temp['ct-ratio'])

test=answer_seven()
test

"""question 8"""
Top15['pop']=Top15['Energy Supply']/Top15['Energy Supply per Capita']
temp=Top15.sort_values(by='pop',ascending=False).iloc[2]
temp.name
Top15.sort_values(by='pop',ascending=False).head() 

def answer_eight():
    Top15 = answer_one()
    Top15['pop']=Top15['Energy Supply']/Top15['Energy Supply per Capita']
    temp=Top15.sort_values(by='pop',ascending=False).iloc[2]
    return (temp.name)


"""question 9"""
def plot9():
    import matplotlib as plt
    %matplotlib inline
    
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15.plot(x='Citable docs per Capita', y='Energy Supply per Capita', kind='scatter', xlim=[0, 0.0006])


plot9()


    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15[['PopEst','Citable docs per Capita']].corr().iloc[0,1]
    
    
def answer_nine():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    Top15[['PopEst','Citable docs per Capita']].corr().iloc[0,1]
    return Top15[['PopEst','Citable docs per Capita']].corr().iloc[0,1]

test=answer_nine()
test

"""question 10"""

median_renew=Top15['% Renewable'].median()  
Top15['HighRenew']=np.where(Top15['% Renewable']>=median_renew,1,0)
Top15.sort_values(by='Rank',ascending=True,inplace=True)
Top15[['% Renewable','Rank']]

def answer_ten():
    Top15 = answer_one()
    median_renew=Top15['% Renewable'].median()  
    Top15['HighRenew']=np.where(Top15['% Renewable']>=median_renew,1,0)
    Top15.sort_values(by='Rank',ascending=True,inplace=True)
    return Top15['% Renewable']

test=answer_ten()
test

"""question 11"""
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15.reset_index(inplace=True)
    Top15['Continent']=[ContinentDict[i] for i in Top15['Country']]
    Top15['pop'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    #Top15.set_index('Continent').groupby(level=0)['pop'].agg({'size':['count'],'sum':np.sum, 'mean':np.mean,'std':np.std})
    Top15.set_index('Continent').groupby(level=0)['pop'].agg({'size':np.size,'sum':np.sum, 'mean':np.mean,'std':np.std})
    
    temp = pd.DataFrame(columns = ['size', 'sum', 'mean', 'std'])
    
    for group, frame in Top15.groupby(ContinentDict):
        print(group)
        temp.loc[group] = [len(frame), frame['pop'].sum(),frame['pop'].mean(),frame['pop'].std()]

Top15.head()
   
def answer_eleven():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    temp = pd.DataFrame(columns = ['size', 'sum', 'mean', 'std'])
    Top15['pop'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    for group, frame in Top15.groupby(ContinentDict):
        temp.loc[group] = [len(frame), frame['pop'].sum(),frame['pop'].mean(),frame['pop'].std()]
    return temp



def answer_eleven():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    Top15.reset_index(inplace=True)
    Top15['Continent']=[ContinentDict[i] for i in Top15['Country']]
    Top15['pop'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    return Top15.set_index('Continent').groupby(level=0)['pop'].agg({'size':np.size,'sum':np.sum, 'mean':np.mean,'std':np.std})


test=answer_eleven()
test

"""question 12"""
Top15 = answer_one()
ContinentDict  = {'China':'Asia', 
          'United States':'North America', 
          'Japan':'Asia', 
          'United Kingdom':'Europe', 
          'Russian Federation':'Europe', 
          'Canada':'North America', 
          'Germany':'Europe', 
          'India':'Asia',
          'France':'Europe', 
          'South Korea':'Asia', 
          'Italy':'Europe', 
          'Spain':'Europe', 
          'Iran':'Asia',
          'Australia':'Australia', 
          'Brazil':'South America'}
Top15=Top15.reset_index()
Top15['Continent']=[ContinentDict[i] for i in Top15['Country']]
Top15['bins']=pd.cut(Top15['% Renewable'],5)
Top15.groupby(['Continent','bins']).size()

def answer_twelve():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
          'United States':'North America', 
          'Japan':'Asia', 
          'United Kingdom':'Europe', 
          'Russian Federation':'Europe', 
          'Canada':'North America', 
          'Germany':'Europe', 
          'India':'Asia',
          'France':'Europe', 
          'South Korea':'Asia', 
          'Italy':'Europe', 
          'Spain':'Europe', 
          'Iran':'Asia',
          'Australia':'Australia', 
          'Brazil':'South America'}
    Top15=Top15.reset_index()
    Top15['Continent']=[ContinentDict[i] for i in Top15['Country']]
    Top15['bins']=pd.cut(Top15['% Renewable'],5)
    return Top15.groupby(['Continent','bins']).size()

test=answer_twelve()
test

"""question 13"""
def answer_thirteen():
    Top15 = answer_one()
    Top15['pop'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    return Top15['pop'].apply(lambda x: '{0:,}'.format(x))


test=answer_thirteen()
test

def plot_optional():
    import matplotlib as plt
    %matplotlib inline
    Top15 = answer_one()
    ax = Top15.plot(x='Rank', y='% Renewable', kind='scatter', 
                    c=['#e41a1c','#377eb8','#e41a1c','#4daf4a','#4daf4a','#377eb8','#4daf4a','#e41a1c',
                       '#4daf4a','#e41a1c','#4daf4a','#4daf4a','#e41a1c','#dede00','#ff7f00'], 
                    xticks=range(1,16), s=6*Top15['2014']/10**10, alpha=.75, figsize=[16,6]);

    for i, txt in enumerate(Top15.index):
        ax.annotate(txt, [Top15['Rank'][i], Top15['% Renewable'][i]], ha='center')

    print("This is an example of a visualization that can be created to help understand the data. This is a bubble chart showing % Renewable vs. Rank. The size of the bubble corresponds to the countries' 2014 GDP, and the color corresponds to the continent.")
    
plot_optional()
