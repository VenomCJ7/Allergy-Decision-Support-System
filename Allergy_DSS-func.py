#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import pandas as pd
import os

sys.path.insert(0, 'F:\Vishu\BITS\Image Analysis Project') ## referencing pyds.py
import pyds
from pyds import MassFunction
from itertools import product


# In[ ]:


#input_arr is the test data (in array of strings)
#bpa_data is the base data you want to use(out of 8 possible databases) (in dataframe format)



##### to convert bpa csv to bpa df #######
# bpa_data = pd.read_csv(r'F:\Vishu\BITS\Image Analysis Project\new_bpa\Full train\bpa_conf_full.csv')
# bpa_data.set_index('A/C', inplace=True)




# all class names have to be in this format 'R', 'O', 'N', 'RU', 'U', 'UO', 'RO'
# RH, UT, OT, NORMAL, RH_U, RH_O, UT_O
# 8 bpas


# In[8]:


#returns final probability values for one instance
#see how to input bpa_data above

def DSS(input_arr, bpa_data):
    
    #put path to allergy test
    #this puts all the allergen and symptom names in a list (list_col)
    test = pd.read_csv(r'F:\Vishu\BITS\Image Analysis Project\new_test\allergy_test.csv')
    temp_test = test.iloc[:,:-1]
    list_col = list(temp_test.columns)
    
    df = bpa_data
    
    x_test = input_arr
    
    c=0
    test_bpa_single = []
    for a in x_test:
        if(c == len(list_col)):
            break
        if(str(a)=='KR'): 
            c+=1
            continue
        else: 
            s = str(list_col[c])+" "+str(a)
            if(s in df.index):
                for i in range(len(df.loc[s])):
                    if(df.loc[s][i]==0): df.loc[s][i]+=0.0001
                test_bpa_single.append(dict(df.loc[s]))
            else:
                test_bpa_single.append(dict(pd.Series([0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001], index=['R', 'O', 'N', 'RU', 'U', 'UO', 'RO'], name=s)))
            c += 1
            
            
    initial = MassFunction(test_bpa_single[0])
    for i in range(1, len(test_bpa_single)):
        initial = initial&MassFunction(test_bpa_single[i])
        
    #sort_orders = sorted(initial.items(), key=lambda x: x[1], reverse=True)
    #return sort_orders
    return initial


# In[9]:





# In[ ]:




