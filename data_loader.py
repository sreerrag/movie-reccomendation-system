#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd

def load_dataset(file_path, columns):
    data = pd.read_csv(file_path, sep="\t", names=columns)
    return data

def load_item_data(name_path):
    name_data = pd.read_csv(name_path, sep="|", encoding='ISO-8859-1')
    return name_data

