#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import pandas as pd

def create_user_item_matrix(data):
    num_users = len(data["user_id"].unique())
    num_items = len(data["item_id"].unique())
    user_item_matrix = np.zeros((num_users, num_items))
    for index, row in data.iterrows():
        user_id = row["user_id"] - 1
        item_id = row["item_id"] - 1
        user_item_matrix[user_id, item_id] = row["rating"]
    return user_item_matrix

def map_item_ids_to_names(name_data):
    item_id_to_name = {}
    for index, row in name_data.iterrows():
        movie_name = row[1]
        item_id_to_name[row[0]] = movie_name
    return item_id_to_name

