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

class Search(Resource): 
    def get(self, keywords):
        # keywords = (request.get_json()['keywords']).lower()
        print(keywords)
        ke = KeywordExtractor(0)
        keywords_processed = ke.pre_process_single(keywords)
        # first get all the resources 
        resources = ResourceModel.query.all()
        resources = resources_schema.dump(resources)
        # Check for any matches 
        matches = []
        for resource in resources: 
            title = (resource['title']).lower()
            if keywords == title: 
                matches.append(resource)
            # now check for matching keywords
            res_keywords = resource['tags'].split(",")
            print(res_keywords)
            match = 0 
            total = len(res_keywords)
            print(keywords_processed)
            for r in res_keywords:
                # remove trailing and leading whitespaces
                r = r.strip()
                if r in keywords_processed: 
                    match += 1 
            threshold = match/total
            print(threshold)
            # At least 40% of keywords must match 
            if threshold >= 0.4:
                matches.append(resource)
        return {'status': 'success', 'data': matches}, 200
        
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



