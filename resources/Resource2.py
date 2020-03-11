from flask import request
from flask_restful import Resource
from models.Model import db
from models.ResourceModel2 import ResourceModel2, ResourceSchema2
from models.Bookmarks import BookmarksModel, BookmarksSchema
from search.Search import Search
from search.preprocess import preprocess

resources_schema = ResourceSchema2(many=True)
resource_schema = ResourceSchema2()
bookmarks_schema = BookmarksSchema(many=True)
bookmark = BookmarksSchema()

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
    def get(self, user_id):
        """ Returns all resources in DB and whether it has been
         bookmarked by a user
        """
        # First get all the bookmarked resources 
        bookmarks = BookmarksModel.query.filter_by(user_id=user_id)
        bookmarks = bookmarks_schema.dump(bookmarks) # list of dicts 

        # Now get all the resources 
        resources = ResourceModel2.query.all()
        resources = resources_schema.dump(resources) # list of dicts 

        # Now we need to add a field to indicate whether the resource
        # has been bookmarked by the user 
        for resource in resources:
            res_id = resource['id']
            resource['is_bookmarked'] = False
            for bookmark in bookmarks: 
                if res_id == bookmark['resource_id']:
                    resource['is_bookmarked'] = True
        return {'status': 'success','data': resources}, 200

class Resource2Create(Resource): 
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