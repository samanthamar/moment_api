from flask import Blueprint
from flask_restful import Api
from resources.User import UserResource
# from resources.ResResource import ResResource, Search
from resources.Goal import GoalResource, GoalList
from resources.Subgoal import SubgoalResource, SubgoalsResource
from resources.Reflection import ReflectionResource, ReflectionList
from resources.Keyword import KeywordResource
from resources.CrawledData import CrawledRawDataResource
from resources.Resource2 import Search2, Resource2, Resource2Create
from resources.Bookmarks import Bookmarks, BookmarkResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(UserResource, '/users')
# DEPRECATE 
# api.add_resource(ResResource, '/resources') # get resource 
# api.add_resource(Search, '/resources/<keywords>') # search resources ie. localhost:5000/api/search/parent+aac+iphone+blog+ios
api.add_resource(GoalResource, '/goals') # Create goals and generate keywords
api.add_resource(GoalList, '/goals/<user_id>/<complete_status>') # Get all goals and subgoals
api.add_resource(SubgoalResource, '/subgoals') # create subgoals, edit subgoals
api.add_resource(SubgoalsResource, '/subgoals/<goal_id>') # get subgoals based on goal_id
api.add_resource(ReflectionResource, '/reflections') # create reflections
api.add_resource(ReflectionList, '/reflections/<user_id>') # get all reflections
api.add_resource(KeywordResource, '/keywords') # post to get keywords
api.add_resource(CrawledRawDataResource, '/crawledrawdata') # add text file to database
# NEW RESOURCES ROUTES
api.add_resource(Resource2Create, '/resource2') # add new resource
api.add_resource(Resource2, '/resource2/<user_id>') # get all resources for user, indicate whether it has been bookmarked
api.add_resource(Search2, '/search2/<user_id>/<query>') # query a resource 
# NEW BOOKMARKS ROUTES 
api.add_resource(Bookmarks, '/bookmarks/<user_id>') # get all bookmarks for user 
api.add_resource(BookmarkResource, '/bookmarks') # bookmark/unbookmark a resource 
