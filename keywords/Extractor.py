import re
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Create stopwords 
stop_words = set(stopwords.words("english"))

class KeywordExtractor:
    def __init__(self, num_keywords):
        self.num_keywords = num_keywords 
    
    def pre_process(self, docs): 
        """

        :param docs: a list of docs to process
        :return: corpus of text processed docs
        """
        corpus = []
        print(corpus)
        for d in docs:
            # Remove puncuation
            text = re.sub('[^a-zA-Z]', ' ', d)
            # Convert to lowercase
            text = text.lower()
            # Remove tags
            text = re.sub("&lt;/?.*?&gt;", " &lt;&gt; ", text)
            # remove special characters and digits
            text = re.sub("(\\d|\\W)+", " ", text)
            ##Convert to list from string
            text = text.split()
            ##Stemming
            ps = PorterStemmer()
            # Lemmatisation
            lem = WordNetLemmatizer()
            text = [lem.lemmatize(word) for word in text if not word in
                                                                stop_words]
            text = " ".join(text)
            corpus.append(text)
        return corpus
    
    def create_tfidf_vectors(self, corpus): 
        """

        :param corpus: corpus to apply tfidf to
        :return: tuple of tfidf vectors for all items in corpus and feature names  
        """
        tfidf_vectorizer = TfidfVectorizer(use_idf=True, stop_words=stop_words)
        # All tfidf vectors
        tfidf_vectorizer_vectors = tfidf_vectorizer.fit_transform(corpus)
        # Get feature names 
        feature_names = tfidf_vectorizer.get_feature_names()
        return (tfidf_vectorizer_vectors, feature_names) 

    def extract_topn_from_vector(self, tfidf_vectorizer_vecs, feature_names, doc_index): 
        """

        :param tfidf_vectorizer_vecs: a list of all tfidf vecs for items in corpus 
        :param feature_names: a list of all feature names 
        :param doc_index: index of where desired doc is located 
        :return: corpus of text processed docs
        """
        vector_1 = tfidf_vectorizer_vecs[doc_index]
        df = pd.DataFrame(vector_1.T.todense(), index=feature_names, columns=["tfidf"])
        # Get topn keywords 
        keywords = df.sort_values(by=["tfidf"],ascending=False)[:self.num_keywords] 
        return keywords

def testing():
    docs = ["the house had a tiny little mouse",
            "the cat saw the mouse",
            "the mouse ran away from the house",
            "the cat finally ate the mouse",
            "the end of the mouse story"]

    extractor = KeywordExtractor(3) 
    corpus = extractor.pre_process(docs)
    (tfidf_vecs,feature_names) = extractor.create_tfidf_vectors(corpus)
    # Dataframe 
    keywords = extractor.extract_topn_from_vector(tfidf_vecs,feature_names, 0)
    print(keywords)

# testing()