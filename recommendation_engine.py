#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
from sklearn.decomposition import TruncatedSVD

class SVDRecommendationEngine:
    def __init__(self, user_item_matrix):
        self.user_item_matrix = user_item_matrix
        self.svd = TruncatedSVD(n_components=10)
        self.user_features = self.svd.fit_transform(self.user_item_matrix)

    def generate_recommendations(self, user_id, item_id_to_name):
        user_features = self.user_features[user_id]
        scores = np.dot(self.user_features, user_features)
        top_items = np.argsort(-scores)[:10]
        recommendations = [' '.join(item_id_to_name[item+1]) for item in top_items]
        return recommendations

