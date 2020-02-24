from flask import request
from flask_restful import Resource
from models.Model import db
from models.ResourceModel import ResourceModel, ResourceSchema
from models.CrawledRawData import CrawledRawDataSchema, CrawledRawData
from keywords.Extractor import KeywordExtractor

resources_schema = ResourceSchema(many=True)
resource_schema = ResourceSchema()
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

class ResResource(Resource):
    def get(self):
        """ Gets all resources in database
        """
        resources = ResourceModel.query.all()
        resources = resources_schema.dump(resources)
        return {'status': 'success', 'data': resources}, 200

    def post(self): 
        """ Stores raw text in db and stores the resource info
        """
        print('you are here')
        text = request.form['text']
        link = request.form['link']
        title = request.form['title']
        num_keywords = int(request.form['num_keywords'])
        # Begin extraction 
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
        # Store the text in the DB 
        new_text = CrawledRawData(text=text)
        db.session.add(new_text)
        # Store resource data in db 
        new_resource = ResourceModel(title=title, 
            link=link, 
            tags=keywords)
        db.session.add(new_resource)
        # Commit both DB transactions 
        db.session.commit()
        return {'status': 'success','resource': resource_schema.dump(new_resource)}, 200



