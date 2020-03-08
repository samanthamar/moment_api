import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from models.ResourceModel2 import ResourceModel2, ResourceSchema2
# resources_schema = ResourceSchema2(many=True)
# resource_schema = ResourceSchema2()

class Search:
    def __init__(self, query):
        self.query = query 

    def tfidf(self, resources): 
        # create the dataframe from list of dicts
        df = pd.DataFrame(resources)
        # print(df)
        # Create the tfidf vectorizer
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(df['text'])
        # Vectorize the query
        query_vec = vectorizer.transform([self.query])
        # Cosine similarity 
        results = cosine_similarity(X,query_vec).reshape((-1,))
        matches = []
        # Return top 10 
        for i in results.argsort()[-10:][::-1]:
            print(df)
            matches.append({'res_id': int(df.iloc[i]['id']), 'title':df.iloc[i]['title']})
        return matches 