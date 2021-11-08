#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
import pandas as pd
import os
import numpy as np
import math
from math import isnan
import copy

sys.path.insert(0, 'F:\Vishu\BITS\Image Analysis Project')
import pyds
from pyds import MassFunction
from itertools import product


# In[2]:


test = pd.read_csv(r'F:\Vishu\BITS\Image Analysis Project\new_test\allergy_test.csv')
x_test = test.iloc[:,:-1]
y_test = test.iloc[:,-1]


for i in range(len(y_test)):
    if y_test[i]=='RH': y_test[i] = 'R'
    elif y_test[i]=='UT': y_test[i] = 'U'
    elif y_test[i]=='OT': y_test[i] = 'O'
    elif y_test[i]=='RH_UT': y_test[i] = 'RU'
    elif y_test[i]=='RH_O': y_test[i] = 'RO'
    elif y_test[i]=='UT_O': y_test[i] = 'UO'
    elif y_test[i]=='NORMAL': y_test[i] = 'N'


# <font size = 4>Full train</font> 

# In[3]:


#confidence full

df = pd.read_csv(r'F:\Vishu\BITS\Image Analysis Project\new_bpa\Full train\bpa_conf_full.csv')
df.set_index('A/C', inplace=True)

list_col = list(x_test.columns)
symptoms = ['runningnose', 'sneeze', 'cough', 'wheezeBlocks', 'headache', 'itching', 'swelling', 'redrashes', 'Fhistory']
test_bpa_full = []
for row in x_test.iterrows():
    c = 0
    test_bpa_single = []
    for a in row[1]:
        if(c == len(x_test.columns)):
            break
        if str(list_col[c]) in symptoms: 
            s = str(list_col[c])+" "+str(a)
            if(s in df.index):
                for i in range(len(df.loc[s])):
                    if(df.loc[s][i]==0): df.loc[s][i]+=0.0001
                test_bpa_single.append(dict(df.loc[s]))
                #print(test_bpa_single)
            else:
                test_bpa_single.append(dict(pd.Series([0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001], index=['R', 'O', 'N', 'RU', 'U', 'UO', 'RO'], name=s)))
            c += 1
        else:
            c+=1
            continue
    test_bpa_full.append(test_bpa_single)


# In[4]:


acc = 0
for i in range(len(test_bpa_full)):
    initial = MassFunction(test_bpa_full[i][0])
    for j in range(1, len(test_bpa_full[i])):
        initial = initial&MassFunction(test_bpa_full[i][j])
        
    pred_label = []
    sort_orders = sorted(initial.items(), key=lambda x: x[1], reverse=True)
    if (str(list(sort_orders[3][0])[0])=='N'): pred_label = ['N']
    elif(initial['R']>0.8 and initial['R']<0.9):
        temp=""
        for i in range(2):
            temp+=str(list(sort_orders[i][0])[0])
        pred_label = [temp]
    else: pred_label=list(initial.max_pl())
    
    if(pred_label[0] in y_test[i] or y_test[i] in pred_label[0]): acc+=1
    
print("Confidence Full Data Accuracy = ", acc/len(test_bpa_full)) 


# In[5]:


#support full

df = pd.read_csv(r'F:\Vishu\BITS\Image Analysis Project\new_bpa\Full train\bpa_support_full.csv')
df.set_index('A/C', inplace=True)

list_col = list(x_test.columns)
symptoms = ['runningnose', 'sneeze', 'cough', 'wheezeBlocks', 'headache', 'itching', 'swelling', 'redrashes', 'Fhistory']
test_bpa_full = []
for row in x_test.iterrows():
    c = 0
    test_bpa_single = []
    for a in row[1]:
        if(c == len(x_test.columns)):
            break
        if str(list_col[c]) in symptoms: 
            s = str(list_col[c])+" "+str(a)
            if(s in df.index):
                for i in range(len(df.loc[s])):
                    if(df.loc[s][i]==0): df.loc[s][i]+=0.0001
                test_bpa_single.append(dict(df.loc[s]))
                #print(test_bpa_single)
            else:
                test_bpa_single.append(dict(pd.Series([0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001], index=['R', 'O', 'N', 'RU', 'U', 'UO', 'RO'], name=s)))
            c += 1
        else:
            c+=1
            continue
    test_bpa_full.append(test_bpa_single)


# In[6]:


acc = 0
for i in range(len(test_bpa_full)):
    initial = MassFunction(test_bpa_full[i][0])
    for j in range(1, len(test_bpa_full[i])):
        initial = initial&MassFunction(test_bpa_full[i][j])
        
    pred_label = []
    sort_orders = sorted(initial.items(), key=lambda x: x[1], reverse=True)
    if (str(list(sort_orders[3][0])[0])=='N'): pred_label = ['N']
    elif(initial['R']>0.8 and initial['R']<0.9):
        temp=""
        for i in range(2):
            temp+=str(list(sort_orders[i][0])[0])
        pred_label = [temp]
    else: pred_label=list(initial.max_pl())

    if(pred_label[0] in y_test[i] or y_test[i] in pred_label[0]): acc+=1
    
print("Support Full Data Accuracy = ", acc/len(test_bpa_full)) 


# <font size = 4>Singleton train</font> 

# In[7]:


#confidence singleton

df = pd.read_csv(r'F:\Vishu\BITS\Image Analysis Project\new_bpa\Singleton train\bpa_conf_singleton.csv')
df.set_index('A/C', inplace=True)

list_col = list(x_test.columns)
symptoms = ['runningnose', 'sneeze', 'cough', 'wheezeBlocks', 'headache', 'itching', 'swelling', 'redrashes', 'Fhistory']
test_bpa_full = []
for row in x_test.iterrows():
    c = 0
    test_bpa_single = []
    for a in row[1]:
        if(c == len(x_test.columns)):
            break
        if str(list_col[c]) in symptoms: 
            s = str(list_col[c])+" "+str(a)
            if(s in df.index):
                for i in range(len(df.loc[s])):
                    if(df.loc[s][i]==0): df.loc[s][i]+=0.0001
                test_bpa_single.append(dict(df.loc[s]))
                #print(test_bpa_single)
            else:
                test_bpa_single.append(dict(pd.Series([0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001], index=['R', 'O', 'N', 'RU', 'U', 'UO', 'RO'], name=s)))
            c += 1
        else:
            c+=1
            continue
    test_bpa_full.append(test_bpa_single)


# In[8]:


acc = 0
for i in range(len(test_bpa_full)):
    initial = MassFunction(test_bpa_full[i][0])
    for j in range(1, len(test_bpa_full[i])):
        initial = initial&MassFunction(test_bpa_full[i][j])
        
    pred_label = []
    sort_orders = sorted(initial.items(), key=lambda x: x[1], reverse=True)
    if (str(list(sort_orders[3][0])[0])=='N'): pred_label = ['N']
    elif(initial['R']>0.8 and initial['R']<0.9):
        temp=""
        for i in range(2):
            temp+=str(list(sort_orders[i][0])[0])
        pred_label = [temp]
    else: pred_label=list(initial.max_pl())

    if(pred_label[0] in y_test[i] or y_test[i] in pred_label[0]): acc+=1
    
print("Confidence Singleton Data Accuracy = ", acc/len(test_bpa_full)) 


# In[9]:


#support singleton

df = pd.read_csv(r'F:\Vishu\BITS\Image Analysis Project\new_bpa\Singleton train\bpa_support_singleton.csv')
df.set_index('A/C', inplace=True)

list_col = list(x_test.columns)
symptoms = ['runningnose', 'sneeze', 'cough', 'wheezeBlocks', 'headache', 'itching', 'swelling', 'redrashes', 'Fhistory']
test_bpa_full = []
for row in x_test.iterrows():
    c = 0
    test_bpa_single = []
    for a in row[1]:
        if(c == len(x_test.columns)):
            break
        if str(list_col[c]) in symptoms: 
            s = str(list_col[c])+" "+str(a)
            if(s in df.index):
                for i in range(len(df.loc[s])):
                    if(df.loc[s][i]==0): df.loc[s][i]+=0.0001
                test_bpa_single.append(dict(df.loc[s]))
                #print(test_bpa_single)
            else:
                test_bpa_single.append(dict(pd.Series([0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001], index=['R', 'O', 'N', 'RU', 'U', 'UO', 'RO'], name=s)))
            c += 1
        else:
            c+=1
            continue
    test_bpa_full.append(test_bpa_single)


# In[10]:


acc = 0
for i in range(len(test_bpa_full)):
    initial = MassFunction(test_bpa_full[i][0])
    for j in range(1, len(test_bpa_full[i])):
        initial = initial&MassFunction(test_bpa_full[i][j])
        
    pred_label = []
    sort_orders = sorted(initial.items(), key=lambda x: x[1], reverse=True)
    if (str(list(sort_orders[3][0])[0])=='N'): pred_label = ['N']
    elif(initial['R']>0.8 and initial['R']<0.9):
        temp=""
        for i in range(2):
            temp+=str(list(sort_orders[i][0])[0])
        pred_label = [temp]
    else: pred_label=list(initial.max_pl())

    if(pred_label[0] in y_test[i] or y_test[i] in pred_label[0]): acc+=1
    
print("Support Singleton Data Accuracy = ", acc/len(test_bpa_full)) 


# <font size = 4>Constant train</font>

# In[11]:


#confidence constant

df = pd.read_csv(r'F:\Vishu\BITS\Image Analysis Project\new_bpa\Const train\bpa_conf_const.csv')
df.set_index('A/C', inplace=True)

list_col = list(x_test.columns)
symptoms = ['runningnose', 'sneeze', 'cough', 'wheezeBlocks', 'headache', 'itching', 'swelling', 'redrashes', 'Fhistory']
test_bpa_full = []
for row in x_test.iterrows():
    c = 0
    test_bpa_single = []
    for a in row[1]:
        if(c == len(x_test.columns)):
            break
        if str(list_col[c]) in symptoms: 
            s = str(list_col[c])+" "+str(a)
            if(s in df.index):
                for i in range(len(df.loc[s])):
                    if(df.loc[s][i]==0): df.loc[s][i]+=0.0001
                test_bpa_single.append(dict(df.loc[s]))
                #print(test_bpa_single)
            else:
                test_bpa_single.append(dict(pd.Series([0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001], index=['R', 'O', 'N', 'RU', 'U', 'UO', 'RO'], name=s)))
            c += 1
        else:
            c+=1
            continue
    test_bpa_full.append(test_bpa_single)


# In[12]:


acc = 0
for i in range(len(test_bpa_full)):
    initial = MassFunction(test_bpa_full[i][0])
    for j in range(1, len(test_bpa_full[i])):
        initial = initial&MassFunction(test_bpa_full[i][j])
        
    pred_label = []
    sort_orders = sorted(initial.items(), key=lambda x: x[1], reverse=True)
    if (str(list(sort_orders[3][0])[0])=='N'): pred_label = ['N']
    elif(initial['R']>0.8 and initial['R']<0.9):
        temp=""
        for i in range(2):
            temp+=str(list(sort_orders[i][0])[0])
        pred_label = [temp]
    else: pred_label=list(initial.max_pl())

    if(pred_label[0] in y_test[i] or y_test[i] in pred_label[0]): acc+=1
    
print("Confidence Constant Data Accuracy = ", acc/len(test_bpa_full)) 


# In[13]:


#support constant

df = pd.read_csv(r'F:\Vishu\BITS\Image Analysis Project\new_bpa\Const train\bpa_support_const.csv')
df.set_index('A/C', inplace=True)

list_col = list(x_test.columns)
symptoms = ['runningnose', 'sneeze', 'cough', 'wheezeBlocks', 'headache', 'itching', 'swelling', 'redrashes', 'Fhistory']
test_bpa_full = []
for row in x_test.iterrows():
    c = 0
    test_bpa_single = []
    for a in row[1]:
        if(c == len(x_test.columns)):
            break
        if str(list_col[c]) in symptoms: 
            s = str(list_col[c])+" "+str(a)
            if(s in df.index):
                for i in range(len(df.loc[s])):
                    if(df.loc[s][i]==0): df.loc[s][i]+=0.0001
                test_bpa_single.append(dict(df.loc[s]))
                #print(test_bpa_single)
            else:
                test_bpa_single.append(dict(pd.Series([0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001], index=['R', 'O', 'N', 'RU', 'U', 'UO', 'RO'], name=s)))
            c += 1
        else:
            c+=1
            continue
    test_bpa_full.append(test_bpa_single)


# In[14]:


acc = 0
for i in range(len(test_bpa_full)):
    initial = MassFunction(test_bpa_full[i][0])
    for j in range(1, len(test_bpa_full[i])):
        initial = initial&MassFunction(test_bpa_full[i][j])
        
    pred_label = []
    sort_orders = sorted(initial.items(), key=lambda x: x[1], reverse=True)
    if (str(list(sort_orders[3][0])[0])=='N'): pred_label = ['N']
    elif(initial['R']>0.8 and initial['R']<0.9):
        temp=""
        for i in range(2):
            temp+=str(list(sort_orders[i][0])[0])
        pred_label = [temp]
    else: pred_label=list(initial.max_pl())

    if(pred_label[0] in y_test[i] or y_test[i] in pred_label[0]): acc+=1
    
print("Support Constant Data Accuracy = ", acc/len(test_bpa_full)) 


# <font size = 4>Unbalanced train</font>

# In[15]:


#confidence unbalanced

df = pd.read_csv(r'F:\Vishu\BITS\Image Analysis Project\new_bpa\Ub train\bpa_conf_ub.csv')
df.set_index('A/C', inplace=True)

list_col = list(x_test.columns)
symptoms = ['runningnose', 'sneeze', 'cough', 'wheezeBlocks', 'headache', 'itching', 'swelling', 'redrashes', 'Fhistory']
test_bpa_full = []
for row in x_test.iterrows():
    c = 0
    test_bpa_single = []
    for a in row[1]:
        if(c == len(x_test.columns)):
            break
        if str(list_col[c]) in symptoms: 
            s = str(list_col[c])+" "+str(a)
            if(s in df.index):
                for i in range(len(df.loc[s])):
                    if(df.loc[s][i]==0): df.loc[s][i]+=0.0001
                test_bpa_single.append(dict(df.loc[s]))
                #print(test_bpa_single)
            else:
                test_bpa_single.append(dict(pd.Series([0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001], index=['R', 'O', 'N', 'RU', 'U', 'UO', 'RO'], name=s)))
            c += 1
        else:
            c+=1
            continue
    test_bpa_full.append(test_bpa_single)


# In[16]:


acc = 0
for i in range(len(test_bpa_full)):
    initial = MassFunction(test_bpa_full[i][0])
    for j in range(1, len(test_bpa_full[i])):
        initial = initial&MassFunction(test_bpa_full[i][j])
        
    pred_label = []
    sort_orders = sorted(initial.items(), key=lambda x: x[1], reverse=True)
    if (str(list(sort_orders[3][0])[0])=='N'): pred_label = ['N']
    elif(initial['R']>0.8 and initial['R']<0.9):
        temp=""
        for i in range(2):
            temp+=str(list(sort_orders[i][0])[0])
        pred_label = [temp]
    else: pred_label=list(initial.max_pl())

    if(pred_label[0] in y_test[i] or y_test[i] in pred_label[0]): acc+=1
    
print("Confidence Unbalanced Data Accuracy = ", acc/len(test_bpa_full)) 


# In[17]:


#Support unbalanced

df = pd.read_csv(r'F:\Vishu\BITS\Image Analysis Project\new_bpa\Ub train\bpa_support_ub.csv')
df.set_index('A/C', inplace=True)

list_col = list(x_test.columns)
symptoms = ['runningnose', 'sneeze', 'cough', 'wheezeBlocks', 'headache', 'itching', 'swelling', 'redrashes', 'Fhistory']
test_bpa_full = []
for row in x_test.iterrows():
    c = 0
    test_bpa_single = []
    for a in row[1]:
        if(c == len(x_test.columns)):
            break
        if str(list_col[c]) in symptoms: 
            s = str(list_col[c])+" "+str(a)
            if(s in df.index):
                for i in range(len(df.loc[s])):
                    if(df.loc[s][i]==0): df.loc[s][i]+=0.0001
                test_bpa_single.append(dict(df.loc[s]))
                #print(test_bpa_single)
            else:
                test_bpa_single.append(dict(pd.Series([0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.0001], index=['R', 'O', 'N', 'RU', 'U', 'UO', 'RO'], name=s)))
            c += 1
        else:
            c+=1
            continue
    test_bpa_full.append(test_bpa_single)


# In[18]:


acc = 0
for i in range(len(test_bpa_full)):
    initial = MassFunction(test_bpa_full[i][0])
    for j in range(1, len(test_bpa_full[i])):
        initial = initial&MassFunction(test_bpa_full[i][j])
        
    pred_label = []
    sort_orders = sorted(initial.items(), key=lambda x: x[1], reverse=True)
    if (str(list(sort_orders[3][0])[0])=='N'): pred_label = ['N']
    elif(initial['R']>0.8 and initial['R']<0.9):
        temp=""
        for i in range(2):
            temp+=str(list(sort_orders[i][0])[0])
        pred_label = [temp]
    else: pred_label=list(initial.max_pl())

    if(pred_label[0] in y_test[i] or y_test[i] in pred_label[0]): acc+=1
    
print("Support Unbalanced Data Accuracy = ", acc/len(test_bpa_full)) 

