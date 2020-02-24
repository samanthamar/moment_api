from flask import request
from flask_restful import Resource
from models.Model import db
from models.ResourceModel import ResourceModel, ResourceSchema
from models.CrawledRawData import CrawledRawDataSchema, CrawledRawData
from keywords.Extractor import KeywordExtractor

texts_schema = CrawledRawDataSchema(many=True)
text_schema = CrawledRawDataSchema()

def getAllResources(): 
    # get all crawled text from DB 
    # this is a list of dicts 
    data = CrawledRawData.query.all()
    data = texts_schema.dump(data) 
    docs = []
    # get the text from each crawleddata dict 
    for obj in data: 
        docs.append(obj['text'])
    return docs

class KeywordResource(Resource):
    def post(self):
        """ Returns keywords for a given text 
        """
        text = request.form['text']
        num_keywords = int(request.form['num_keywords'])
        # use this flag for dev! 
        store_in_db = eval(request.form['store_in_db'])
        docs = getAllResources()
        # Add desired text to corpus 
        docs.append(text)
        extractor = KeywordExtractor(num_keywords)
        # Creates a corpus 
        corpus = extractor.pre_process(docs)
        (tfidf_vec, feature_names) = extractor.create_tfidf_vectors(corpus, text)
        # Dataframe
        keywords = extractor.extract_topn_from_vector(tfidf_vec, feature_names)
        # Keywords are indices to pd df, convert it to a list!
        keywords_list = keywords.index.tolist()
        keywords =  ', '.join(keywords_list)
        # Store the crawled text in db if true
        if store_in_db:
            new_text = CrawledRawData(text=text)
            db.session.add(new_text)
            db.session.commit()
            return {'status': 'success', 'keywords': keywords, 'text': text_schema.dump(new_text)}, 200
        return {'status': 'success', 'keywords': keywords}, 200

