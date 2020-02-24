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

    def create_tfidf_vectors(self, corpus, doc):
        """

        :param corpus: corpus to apply tfidf to
        :param doc: doc we want keywords
        :return: tuple of tfidf vectors for all items in corpus and feature names  
        """
        tfidf_vectorizer = TfidfVectorizer(use_idf=True, stop_words=stop_words)
        # All tfidf vectors
        tfidf_vectorizer.fit_transform(corpus)
        # tfidf vector for the particular doc
        tfidf_vec = tfidf_vectorizer.transform([doc])
        # Get feature names 
        feature_names = tfidf_vectorizer.get_feature_names()
        return (tfidf_vec, feature_names)

    def extract_topn_from_vector(self, tfidf_vec, feature_names):
        """

        :param tfidf_vec: tfidf scores for all keywords for a particular doc
        :param feature_names: a list of all feature names
        :return: keywords as a pd dataframe
        """
        df = pd.DataFrame(tfidf_vec.T.todense(), index=feature_names, columns=["tfidf"])
        # Get topn keywords 
        keywords = df.sort_values(by=["tfidf"],ascending=False)[:self.num_keywords] 
        return keywords