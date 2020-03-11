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
    def put(self):
        """ Add or remove a bookmark from a resource
        """
        is_bookmarked = request.get_json()['is_bookmarked'] # expect a bool
        resource_id = request.get_json()['resource_id'] # this can be null if unbookmarking! 
        user_id = request.get_json()['user_id']
        
        if is_bookmarked: 
            # Create a new bookmark
            new_bookmark = BookmarksModel(user_id=user_id, resource_id=resource_id)
            db.session.add(new_bookmark)
            db.session.commit()
            return {'status': 'success', 'message': 'Bookmark successfully added'}, 200
        elif not is_bookmarked: 
            # Delete an existing bookmark
            bookmark_to_del = BookmarksModel.query.filter_by(user_id=user_id, resource_id=resource_id).first()
            db.session.delete(bookmark_to_del)
            db.session.commit()
            return {'status': 'success', 'message': 'Bookmark successfully deleted'}, 200
        