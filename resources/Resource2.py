from flask import request
from flask_restful import Resource
from models.Model import db
from models.ResourceModel2 import ResourceModel2, ResourceSchema2
from search.Search import Search
from search.preprocess import preprocess

resources_schema = ResourceSchema2(many=True)
resource_schema = ResourceSchema2()

# NOTE: WIP!!! 
class Search2(Resource):
    def get(self, query): 
        """Search for a resource in the DB 
        """
        print(query)
        query = preprocess(query)
        print(query)
        search = Search(query)
        resources = ResourceModel2.query.all()
        resources = resources_schema.dump(resources) 
        matches = search.tfidf(resources) # list of dicts 
        print(matches)
        return {'status': 'success','data': matches}, 200

class Resource2(Resource):
    def get(self):
        """Return all resources in DB 
        """
        data = ResourceModel2.query.all()
        data = resources_schema.dump(data) 
        return {'status': 'success','data': data}, 200

    def post(self): 
        """Add a new resource to DB 
        Text is preprocessed before added to DB
        """
        text = request.form['text']
        title = request.form['title']
        link = request.form['link']
        text = preprocess(text)
        img = request.form['img']
        category = request.form['category']
        print(text)
        # create the resource 
        new_resource = ResourceModel2(title=title, link=link, text=text, img=img, category=category)
        db.session.add(new_resource)
        db.session.commit()
        return {'status': 'success','data': resource_schema.dump(new_resource)}, 200