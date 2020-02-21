from flask import Blueprint
from flask_restful import Api
from resources.User import UserResource
from resources.ResResource import ResResource
from resources.Goal import GoalResource, GoalList
from resources.Subgoal import SubgoalResource
from resources.Reflection import ReflectionResource, ReflectionList

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(UserResource, '/users')
api.add_resource(ResResource, '/resources') # get resource 
api.add_resource(GoalResource, '/goals') # Create goals and generate keywords
api.add_resource(GoalList, '/goals/<user_id>') # Get all goals and subgoals
api.add_resource(SubgoalResource, '/subgoals') # create subgoals 
api.add_resource(ReflectionResource, '/reflections') # create reflections
api.add_resource(ReflectionList, '/reflections/<user_id>') # get all reflections