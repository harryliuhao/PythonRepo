# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 12:26:07 2017

@author: Hao Liu
"""

import pandas as pd

df = pd.DataFrame({"borough":["A", "B", "B", "A", "A"], "title":["Book2", "Book1", "Book2", "Book2", "Book1"], "total_loans":[4, 48, 46, 78, 15]})

top_boroughs = df.groupby(['borough','title'])
top_boroughs.aggregate(sum).sort(['total_loans','title'], ascending=False)

df.groupby('borough')['total_loans'].max()


df.groupby(level=[0,1]).sum().reset_index().sort_values(['borough', 'total_loans'], ascending=[1,0]).groupby('borough').head(3)