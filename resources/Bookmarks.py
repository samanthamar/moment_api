from flask import request
from flask_restful import Resource
from models.Model import db
from models.Bookmarks import BookmarksModel, BookmarksSchema
from models.ResourceModel2 import ResourceSchema2, ResourceModel2

bookmarks_schema = BookmarksSchema(many=True)
bookmark_schema = BookmarksSchema()
resource_schema = ResourceSchema2()

class Bookmarks(Resource): 
    def get(self, user_id): 
        """ Return the bookmarks for a given user
        """
        # Get all bookmarks for user
        bookmarks = BookmarksModel.query.filter_by(user_id=user_id)
        # Iterate through bookmarks 
        res_ids = []
        for bookmark in bookmarks:
            res_ids.append(bookmark.resource_id)
        # Get all the resources associated with the res_ids 
        resources = []
        for res_id in res_ids: 
            res = ResourceModel2.query.filter_by(id=res_id).first()
            # Dump the resource to a dict 
            res = resource_schema.dump(res)
            resources.append(res)
        return {'status': 'success', 'data': resources}, 200
            
class BookmarkResource(Resource):
    def put(self, user_id, resource_id, action): 
        """ Bookmark or unbookmark a resource 
        """
        if action == 'bookmark':
            new_bookmark = BookmarksModel(user_id=user_id, resource_id=resource_id)
            db.session.add(new_bookmark)
        elif action == 'unbookmark':
            # first get the bookmark id 
            bookmark_to_del = BookmarksModel.query.filter_by(user_id=user_id, resource_id=resource_id).first()
            db.session.delete(bookmark_to_del)
        else:
           return {'status': 'error', 'message': 'unsupported action'}, 400
        db.session.commit()
        return {'status': 'success'}, 200
        