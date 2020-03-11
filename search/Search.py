import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.ResourceModel2 import ResourceModel2, ResourceSchema2

class Search:
    def __init__(self, query):
        self.query = query 

    def tfidf(self, resources): 
        # create the dataframe from list of dicts
        df = pd.DataFrame(resources)
        # Create the tfidf vectorizer
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['text'])
        # Vectorize the query
        query_vec = vectorizer.transform([self.query])
        # Cosine similarity 
        results = cosine_similarity(X,query_vec).reshape((-1,))
        print(results)
        matches = []
        # Return top 10 
        # NOTE: even if score is 0 it may display because of number of documents 
        for i in results.argsort()[-10:][::-1]:
            matches.append({'id': int(df.iloc[i]['id']), 
            'title':df.iloc[i]['title'],
            'link':df.iloc[i]['link'],
            'category':df.iloc[i]['category'],
            'img':df.iloc[i]['img']})
        return matches 